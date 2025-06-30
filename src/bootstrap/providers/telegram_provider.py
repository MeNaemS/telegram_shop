from dishka import Provider, Scope, provide
from aiogram import Bot
import aiohttp
from src.config_schema import Config
from src.application.interfaces.telegram_client import TelegramClientInterface
from src.application.interfaces.image_client import ImageClientInterface
from src.application.interfaces.excel_client import ExcelClientInterface
from src.application.interfaces.payment_client import PaymentClientInterface
from src.infrastructure.telegram.client_impl import AiogramClientImpl
from src.infrastructure.clients.image_client_impl import ImageClientImpl
from src.infrastructure.excel.excel_client_impl import ExcelClientImpl
from src.infrastructure.yookassa.yookassa_client_impl import YooKassaClientImpl
from src.presentation.telegram.services.product_service import ProductService


class TelegramProvider(Provider):
    @provide(scope=Scope.APP)
    async def bot(self, config: Config) -> Bot:
        return Bot(token=config.telegram.token)

    @provide(scope=Scope.APP)
    async def telegram_client(self, bot: Bot, config: Config) -> TelegramClientInterface:
        return AiogramClientImpl(bot=bot, config=config)

    @provide(scope=Scope.APP)
    async def image_client(self) -> ImageClientInterface:
        return ImageClientImpl()

    @provide(scope=Scope.APP)
    async def excel_client(self) -> ExcelClientInterface:
        return ExcelClientImpl()

    @provide(scope=Scope.APP)
    async def payment_client(self, config: Config, session: aiohttp.ClientSession) -> PaymentClientInterface:
        return YooKassaClientImpl(config, session)

    @provide(scope=Scope.APP)
    async def product_service(self, image_client: ImageClientInterface) -> ProductService:
        return ProductService(image_client)
