from aiogram import Bot, Dispatcher
from logging import getLogger, Logger
from asyncio import run
from dishka import AsyncContainer
from dishka.integrations.aiogram import setup_dishka
from src.infrastructure.logging.logger_setup import setup_logger
from src.presentation.telegram.routers.start import start_router
from src.presentation.telegram.routers.catalog import catalog_router
from src.presentation.telegram.routers.cart import cart_router
from src.presentation.telegram.routers.order import order_router
from src.presentation.telegram.routers.faq import faq_router
from src.bootstrap.container import make_container
from src.presentation.telegram.middlewares.subscription_middleware import SubscriptionMiddleware

setup_logger()
logger: Logger = getLogger(__name__)
container: AsyncContainer = make_container()


async def main() -> None:
    dispatcher: Dispatcher = Dispatcher()
    setup_dishka(container, dispatcher)
    dispatcher.include_router(start_router)
    dispatcher.include_router(catalog_router)
    dispatcher.include_router(cart_router)
    dispatcher.include_router(order_router)
    dispatcher.include_router(faq_router)
    subscription_middleware: SubscriptionMiddleware = await container.get(SubscriptionMiddleware)
    dispatcher.message.middleware(subscription_middleware)
    bot: Bot = await container.get(Bot)
    await dispatcher.start_polling(bot)


if __name__ == "__main__":
    run(main())
