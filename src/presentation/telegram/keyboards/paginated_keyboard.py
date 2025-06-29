from typing import List, Optional
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from src.application.dtos.main_menu import CategoryDTO


async def create_paginated_keyboard(
    category_inf: CategoryDTO,
    page: int,
    prefix: str,
    parent_id: Optional[int] = None
) -> InlineKeyboardMarkup:
    buttons: List[List[InlineKeyboardButton]] = []
    

    if prefix == "subcatalog" and parent_id:
        buttons.append([InlineKeyboardButton(
            text="🛍️ Показать товары",
            callback_data=f"products_{parent_id}_0"
        )])
    
    for i in range(0, min(9, len(category_inf.items)), 3):
        row = []
        for j in range(3):
            if i + j < len(category_inf.items):
                item = category_inf.items[i + j]
                callback_data = f"menu_subcatalog_{item.id}_0"
                row.append(
                    InlineKeyboardButton(
                        text=item.name[:20], 
                        callback_data=callback_data
                    )
                )
        buttons.append(row)
    nav_row: List[InlineKeyboardButton] = []
    if page > 0:
        if prefix == "subcatalog":
            nav_row.append(InlineKeyboardButton(text="⬅️", callback_data=f"menu_subcatalog_{parent_id}_{page - 1}"))
        else:
            nav_row.append(InlineKeyboardButton(text="⬅️", callback_data=f"menu_{prefix}_{page - 1}"))
    nav_row.append(InlineKeyboardButton(text=f"{page+1}/{category_inf.total_pages}", callback_data="noop"))
    if page < category_inf.total_pages - 1:
        if prefix == "subcatalog":
            nav_row.append(InlineKeyboardButton(text="➡️", callback_data=f"menu_subcatalog_{parent_id}_{page + 1}"))
        else:
            nav_row.append(InlineKeyboardButton(text="➡️", callback_data=f"menu_{prefix}_{page + 1}"))
    buttons.append(nav_row)
    
    if prefix == "subcatalog":
        buttons.append([InlineKeyboardButton(text="⬆️ К категориям", callback_data="menu_catalog_0")])
    buttons.append([InlineKeyboardButton(text="🏠 Главное меню", callback_data="back_to_main")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)
