from dishka import Provider, Scope, provide
from aiogram import Bot
from src.config_schema import Config
from src.application.interfaces.telegram_client import TelegramClientInterface
from src.application.interfaces.image_client import ImageClientInterface
from src.application.interfaces.excel_client import ExcelClientInterface
from src.infrastructure.telegram.client_impl import AiogramClientImpl
from src.infrastructure.http.image_client_impl import ImageClientImpl
from src.infrastructure.excel.excel_client_impl import ExcelClientImpl


class TelegramProvider(Provider):
    @provide(scope=Scope.APP)
    async def bot(self, config: Config) -> Bot:
        return Bot(token=config.telegram.token)

    @provide(scope=Scope.APP)
    async def telegram_client(self, bot: Bot, config: Config) -> TelegramClientInterface:
        return AiogramClientImpl(bot=bot, config=config)

    @provide(scope=Scope.APP)
    async def image_client(self, config: Config) -> ImageClientInterface:
        return ImageClientImpl(config=config)

    @provide(scope=Scope.APP)
    async def excel_client(self) -> ExcelClientInterface:
        return ExcelClientImpl()
