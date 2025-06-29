from typing import List
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


async def create_subscription_keyboard(channels: List[str]) -> InlineKeyboardMarkup:
    buttons: List[List[InlineKeyboardButton]] = []
    for channel in channels:
        channel_name: str = channel.lstrip('@')
        buttons.append(
            [
                InlineKeyboardButton(
                    text=f"📢 {channel_name}",
                    url="https://t.me/{channel_name}"
                )
            ]
        )
    return InlineKeyboardMarkup(inline_keyboard=buttons)
