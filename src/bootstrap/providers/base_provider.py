from dishka import Provider, provide, Scope
from src.config_schema import Config
from src.config import config


class BaseProvider(Provider):
    @provide(scope=Scope.APP)
    def get_configs(self) -> Config:
        return config
