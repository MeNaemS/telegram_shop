from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


async def create_main_menu_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="❓ FAQ", callback_data="menu_faq_0")],
            [InlineKeyboardButton(text="📦 Каталог", callback_data="menu_catalog_0")],
            [InlineKeyboardButton(text="🛒 Корзина", callback_data="menu_cart_0")]
        ]
    )
