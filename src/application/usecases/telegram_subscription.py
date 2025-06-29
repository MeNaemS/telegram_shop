from src.application.interfaces.telegram_client import TelegramClientInterface


class TelegramSubscriptionUseCase:
    def __init__(self, telegram_client_impl: TelegramClientInterface) -> None:
        self.telegram_client_impl: TelegramClientInterface = telegram_client_impl

    async def check_user_subscription(self, user_id: int) -> bool:
        return await self.telegram_client_impl.check_chat_member(user_id=user_id)
