from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from dishka.integrations.aiogram import inject, FromDishka
from src.application.usecases.register_user import RegisterUserUseCase
from src.presentation.telegram.keyboards.main_menu_keyboard import create_main_menu_keyboard

start_router: Router = Router(name=__name__)


@start_router.message(CommandStart())
@inject
async def start_handler(
    message: Message,
    register_user_use_case: FromDishka[RegisterUserUseCase]
):
    await register_user_use_case.execute(message.from_user.id)
    await message.answer(
        "Добро пожаловать, выберите действие:",
        reply_markup=await create_main_menu_keyboard()
    )


@start_router.callback_query(F.data == "back_to_main")
async def back_to_main_menu(callback: CallbackQuery):
    await callback.message.edit_text(
        "Выберите действие:", reply_markup=await create_main_menu_keyboard()
    )
