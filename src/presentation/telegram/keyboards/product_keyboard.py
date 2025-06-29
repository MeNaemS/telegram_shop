from typing import List
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from src.domain.entities.product import Product


async def create_product_keyboard(
    products: List[Product], 
    current_index: int, 
    category_id: int
) -> InlineKeyboardMarkup:
    buttons: List[List[InlineKeyboardButton]] = []
    
    nav_row: List[InlineKeyboardButton] = []
    if current_index > 0:
        nav_row.append(InlineKeyboardButton(
            text="⬅️ Предыдущий", 
            callback_data=f"product_{category_id}_{current_index - 1}"
        ))
    if current_index < len(products) - 1:
        nav_row.append(InlineKeyboardButton(
            text="Следующий ➡️", 
            callback_data=f"product_{category_id}_{current_index + 1}"
        ))
    
    if nav_row:
        buttons.append(nav_row)
    
    buttons.append([InlineKeyboardButton(
        text="🛒 Добавить в корзину", 
        callback_data=f"add_to_cart_{products[current_index].id}"
    )])
    
    buttons.append([InlineKeyboardButton(
        text="⬅️ К категориям", 
        callback_data="menu_catalog_0"
    )])
    
    buttons.append([InlineKeyboardButton(
        text="🏠 Главное меню", 
        callback_data="back_to_main"
    )])
    
    return InlineKeyboardMarkup(inline_keyboard=buttons)
