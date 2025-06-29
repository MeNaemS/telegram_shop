from dishka import make_async_container
from src.bootstrap.providers.telegram_provider import TelegramProvider
from src.bootstrap.providers.base_provider import BaseProvider
from src.bootstrap.providers.usecases import UseCasesProvider
from src.bootstrap.providers.middlewares import MiddlewareProvider
from src.bootstrap.providers.database import DatabaseProvider
from src.bootstrap.providers.interfaces import InterfacesProvider
from src.bootstrap.providers.mappers import MappersProvider


def make_container():
    return make_async_container(
        TelegramProvider(),
        BaseProvider(),
        UseCasesProvider(),
        MiddlewareProvider(),
        DatabaseProvider(),
        InterfacesProvider(),
        MappersProvider()
    )
