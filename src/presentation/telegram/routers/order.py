from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, Message
from aiogram.fsm.context import FSMContext
from dishka.integrations.aiogram import inject, FromDishka
from src.application.usecases.create_order import CreateOrderUseCase
from src.presentation.telegram.states.cart_states import OrderState

order_router: Router = Router(name=__name__)


@order_router.callback_query(F.data == "checkout")
async def handle_checkout(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text("📝 Введите ваше полное имя:")
    await state.update_data(bot_message_id=callback.message.message_id)
    await state.set_state(OrderState.waiting_name)


@order_router.message(OrderState.waiting_name)
async def handle_name_input(message: Message, state: FSMContext):
    await state.update_data(full_name=message.text)
    await message.delete()
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="❌ Отмена", callback_data="cancel_order")]
    ])
    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')
    
    await message.bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=bot_message_id,
        text="🏠 Введите адрес доставки:",
        reply_markup=keyboard
    )
    await state.set_state(OrderState.waiting_address)


@order_router.message(OrderState.waiting_address)
async def handle_address_input(message: Message, state: FSMContext):
    await state.update_data(address=message.text)
    await message.delete()
    
    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="❌ Отмена", callback_data="cancel_order")]
    ])
    
    await message.bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=bot_message_id,
        text="📱 Введите номер телефона:",
        reply_markup=keyboard
    )
    await state.set_state(OrderState.waiting_phone)


@order_router.message(OrderState.waiting_phone)
async def handle_phone_input(message: Message, state: FSMContext):
    await state.update_data(phone=message.text)
    await message.delete()
    
    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💳 Карта", callback_data="payment_card")],
        [InlineKeyboardButton(text="💵 Наличные", callback_data="payment_cash")],
        [InlineKeyboardButton(text="❌ Отмена", callback_data="cancel_order")]
    ])
    
    await message.bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=bot_message_id,
        text="💰 Выберите способ оплаты:",
        reply_markup=keyboard
    )
    await state.set_state(OrderState.waiting_payment)


@order_router.callback_query(F.data.startswith("payment_"))
@inject
async def handle_payment_selection(
    callback: CallbackQuery,
    state: FSMContext,
    create_order_use_case: FromDishka[CreateOrderUseCase]
):
    payment_method = "Карта" if callback.data == "payment_card" else "Наличные"
    
    data = await state.get_data()
    await create_order_use_case.execute(
        callback.from_user.id,
        data['full_name'],
        data['address'],
        data['phone'],
        payment_method
    )
    
    await state.clear()
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🏠 Главное меню", callback_data="back_to_main")]
    ])
    await callback.message.edit_text("✅ Заказ успешно оформлен!", reply_markup=keyboard)


@order_router.callback_query(F.data == "cancel_order")
async def handle_cancel_order(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🏠 Главное меню", callback_data="back_to_main")]
    ])
    await callback.message.edit_text("❌ Оформление заказа отменено", reply_markup=keyboard)
