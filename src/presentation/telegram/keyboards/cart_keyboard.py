from typing import List
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from src.infrastructure.database.models.orders import CartItem


async def create_cart_keyboard(cart_items: List[CartItem]) -> InlineKeyboardMarkup:
    buttons: List[List[InlineKeyboardButton]] = []
    
    for item in cart_items:
        buttons.append([
            InlineKeyboardButton(
                text=f"❌ {item.product.name} x{item.quantity}",
                callback_data=f"remove_cart_{item.id}"
            )
        ])
    
    buttons.append([InlineKeyboardButton(text="📦 Оформить заказ", callback_data="checkout")])
    buttons.append([InlineKeyboardButton(text="🏠 Главное меню", callback_data="back_to_main")])
    
    return InlineKeyboardMarkup(inline_keyboard=buttons)
