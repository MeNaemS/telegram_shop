from typing import AsyncIterable
from dishka import Provider, provide, Scope
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker
from src.config_schema import Config
from src.infrastructure.database.connection import create_database_engine, create_session_factory


class DatabaseProvider(Provider):
    @provide(scope=Scope.APP)
    async def get_engine(self, config: Config) -> AsyncEngine:
        return await create_database_engine(config)

    @provide(scope=Scope.REQUEST)
    async def get_session(self, engine: AsyncEngine) -> AsyncIterable[AsyncSession]:
        session_factory: async_sessionmaker[AsyncSession] = await create_session_factory(engine)
        async with session_factory() as session:
            yield session
