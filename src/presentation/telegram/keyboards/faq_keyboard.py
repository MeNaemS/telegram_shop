from typing import List
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from src.application.dtos.faq import FAQdto


async def create_faq_keyboard(faq_data: FAQdto, page: int) -> InlineKeyboardMarkup:
    buttons: List[List[InlineKeyboardButton]] = []
    
    for faq in faq_data.items:
        buttons.append([InlineKeyboardButton(
            text=faq.question[:50] + "..." if len(faq.question) > 50 else faq.question,
            callback_data=f"faq_item_{faq.id}"
        )])
    
    nav_row: List[InlineKeyboardButton] = []
    if page > 0:
        nav_row.append(InlineKeyboardButton(text="⬅️", callback_data=f"menu_faq_{page - 1}"))
    nav_row.append(InlineKeyboardButton(text=f"{page+1}/{faq_data.total_pages}", callback_data="noop"))
    if page < faq_data.total_pages - 1:
        nav_row.append(InlineKeyboardButton(text="➡️", callback_data=f"menu_faq_{page + 1}"))
    
    if nav_row:
        buttons.append(nav_row)
    
    buttons.append([InlineKeyboardButton(text="🏠 Главное меню", callback_data="back_to_main")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)
