from aiogram import BaseMiddleware
from aiogram.types import Message
from dishka.integrations.aiogram import FromDishka
from src.application.usecases.telegram_subscription import TelegramSubscriptionUseCase
from src.config_schema import Config
from src.presentation.telegram.keyboards.subscription_keyboard import create_subscription_keyboard


class SubscriptionMiddleware(BaseMiddleware):
    def __init__(
            self,
            telegram_subscription_use_case: FromDishka[TelegramSubscriptionUseCase],
            config: FromDishka[Config]
        ):
        self.telegram_subscription_use_case: TelegramSubscriptionUseCase = telegram_subscription_use_case
        self.config: Config = config

    async def __call__(
            self,
            handler,
            event: Message,
            data
        ):
        is_subscribed: bool = await self.telegram_subscription_use_case.check_user_subscription(
            user_id=event.from_user.id
        )
        if not is_subscribed:
            await event.answer(
                "Чтобы продолжить работу с ботом необходимо подписаться на следующие каналы:",
                reply_markup=await create_subscription_keyboard(self.config.telegram.chats_id)
            )
            return
        return await handler(event, data)
