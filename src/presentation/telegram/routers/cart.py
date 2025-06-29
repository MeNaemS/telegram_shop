from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, Message
from aiogram.fsm.context import FSMContext
from dishka.integrations.aiogram import inject, FromDishka
from src.application.usecases.add_to_cart import AddToCartUseCase
from src.application.usecases.get_cart import GetCartUseCase
from src.application.usecases.remove_from_cart import RemoveFromCartUseCase
from src.presentation.telegram.keyboards.cart_keyboard import create_cart_keyboard
from src.presentation.telegram.states.cart_states import CartState

cart_router: Router = Router(name=__name__)


@cart_router.callback_query(F.data.startswith("add_to_cart_"))
@inject
async def handle_add_to_cart(callback: CallbackQuery, state: FSMContext):
    product_id = int(callback.data.split("_")[-1])
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="❌ Отмена", callback_data="cancel_cart")]
    ])
    
    await callback.message.edit_text(
        "Укажите количество товара:",
        reply_markup=keyboard
    )
    
    await state.set_state(CartState.waiting_quantity)
    await state.update_data(product_id=product_id, message_id=callback.message.message_id)


@cart_router.callback_query(F.data == "cancel_cart")
@inject
async def handle_cancel_cart(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🏠 Главное меню", callback_data="back_to_main")]
    ])
    await callback.message.edit_text("❌ Добавление в корзину отменено", reply_markup=keyboard)


@cart_router.callback_query(F.data.startswith("menu_cart"))
@inject
async def handle_cart(
    callback: CallbackQuery,
    get_cart_use_case: FromDishka[GetCartUseCase]
):
    cart_items = await get_cart_use_case.execute(callback.from_user.id)
    
    if not cart_items:
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🏠 Главное меню", callback_data="back_to_main")]
        ])
        await callback.message.edit_text("🛍️ Ваша корзина пуста", reply_markup=keyboard)
        return
    
    text = "🛍️ Ваша корзина:\n\n"
    total = 0
    
    for item in cart_items:
        item_total = item.product.price * item.quantity
        total += item_total
        text += f"• {item.product.name} x{item.quantity} = {item_total} руб.\n"
    
    text += f"\n💰 Итого: {total} руб."
    
    keyboard = await create_cart_keyboard(cart_items)
    await callback.message.edit_text(text, reply_markup=keyboard)


@cart_router.message(CartState.waiting_quantity)
@inject
async def handle_quantity_input(
    message: Message,
    state: FSMContext,
    add_to_cart_use_case: FromDishka[AddToCartUseCase]
):
    try:
        quantity = int(message.text)
        if quantity <= 0:
            await message.reply("Количество должно быть положительным числом")
            return
        
        data = await state.get_data()
        product_id = data.get('product_id')
        message_id = data.get('message_id')
        
        await add_to_cart_use_case.execute(message.from_user.id, product_id, quantity)
        
        await message.delete()
        
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🏠 Главное меню", callback_data="back_to_main")]
        ])
        
        await message.bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=message_id,
            text=f"✅ Товар добавлен в корзину! Количество: {quantity}",
            reply_markup=keyboard
        )
        
        await state.clear()
        
    except ValueError:
        await message.reply("Пожалуйста, введите корректное число")


@cart_router.callback_query(F.data.startswith("remove_cart_"))
@inject
async def handle_remove_from_cart(
    callback: CallbackQuery,
    remove_from_cart_use_case: FromDishka[RemoveFromCartUseCase],
    get_cart_use_case: FromDishka[GetCartUseCase]
):
    cart_item_id = int(callback.data.split("_")[-1])
    await remove_from_cart_use_case.execute(callback.from_user.id, cart_item_id)
    await callback.answer("✅ Товар удален из корзины")
    await handle_cart(callback, get_cart_use_case)
