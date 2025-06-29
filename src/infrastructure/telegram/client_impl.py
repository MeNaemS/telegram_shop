from typing import Optional, List
from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest
from src.application.interfaces.telegram_client import TelegramClientInterface
from aiogram.types import ChatFullInfo
from src.config_schema import Config


class AiogramClientImpl(TelegramClientInterface):
    def __init__(self, bot: Bot, config: Config):
        self.bot: Bot = bot
        self.chats_id: List[str] = config.telegram.chats_id

    async def check_chat_member(self, user_id: int) -> bool:
        try:
            collect: List[bool] = []
            for chat_id in self.chats_id:
                member = await self.bot.get_chat_member(chat_id=chat_id, user_id=user_id)
                collect.append(member.status in ["member", "creator", "administrator"])
            return all(collect)
        except TelegramBadRequest:
            return False

    async def send_message(self, chat_id: int, text: str) -> None:
        await self.bot.send_message(chat_id=chat_id, text=text)

    async def get_chat_info(self, chat_id: str) -> Optional[ChatFullInfo]:
        try:
            return await self.bot.get_chat(chat_id=chat_id)
        except TelegramBadRequest:
            return 
