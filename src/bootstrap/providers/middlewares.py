from dishka import Provider, provide, Scope
from src.presentation.telegram.middlewares.subscription_middleware import SubscriptionMiddleware
from src.application.usecases.telegram_subscription import TelegramSubscriptionUseCase
from src.config_schema import Config


class MiddlewareProvider(Provider):
    @provide(scope=Scope.APP)
    async def telegram_subscription_middleware(
        self,
        telegram_subscription_use_case: TelegramSubscriptionUseCase,
        config: Config
    ) -> SubscriptionMiddleware:
        return SubscriptionMiddleware(telegram_subscription_use_case, config)
