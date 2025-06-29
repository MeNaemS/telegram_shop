from abc import ABC, abstractmethod
from typing import Optional


class TelegramClientInterface(ABC):
    @abstractmethod
    async def check_chat_member(self, user_id: int) -> bool:
        ...

    @abstractmethod
    async def send_message(self, chat_id: int, text: str) -> None:
        ...
    
    @abstractmethod
    async def get_chat_info(self, chat_id: str) -> Optional[dict]:
        ...
