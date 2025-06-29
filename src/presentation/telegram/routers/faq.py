from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from dishka.integrations.aiogram import inject, FromDishka
from src.application.usecases.get_faq import GetFAQUseCase
from src.application.usecases.get_faq_by_id import GetFAQByIdUseCase
from src.application.dtos.faq import FAQdto
from src.presentation.telegram.keyboards.faq_keyboard import create_faq_keyboard

faq_router: Router = Router(name=__name__)


@faq_router.callback_query(F.data.startswith("faq_item_"))
@inject
async def handle_faq_item(
    callback: CallbackQuery,
    get_faq_by_id_use_case: FromDishka[GetFAQByIdUseCase]
):
    faq_id = int(callback.data.split("_")[-1])
    faq_item = await get_faq_by_id_use_case.execute(faq_id)
    
    if faq_item:
        text = f"❓ {faq_item.question}\n\n💬 {faq_item.answer}"
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="⬅️ Назад к FAQ", callback_data="menu_faq_0")],
            [InlineKeyboardButton(text="🏠 Главное меню", callback_data="back_to_main")]
        ])
        await callback.message.edit_text(text, reply_markup=keyboard)


@faq_router.callback_query(F.data.startswith("menu_faq"))
@inject
async def handle_faq(
    callback: CallbackQuery,
    get_faq_use_case: FromDishka[GetFAQUseCase]
):
    page = 0
    if "_" in callback.data and callback.data.split("_")[-1].isdigit():
        page = int(callback.data.split("_")[-1])
    
    faq_data: FAQdto = await get_faq_use_case.execute(page)
    keyboard = await create_faq_keyboard(faq_data, page)
    await callback.message.edit_text("❓ Часто задаваемые вопросы:", reply_markup=keyboard)
