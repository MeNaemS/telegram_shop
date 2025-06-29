from dishka import Provider, provide, Scope
from src.application.mappers.main_menu_mapper import CategoryMapper


class MappersProvider(Provider):
    @provide(scope=Scope.APP)
    async def get_category_mapper(self) -> CategoryMapper:
        return CategoryMapper()
