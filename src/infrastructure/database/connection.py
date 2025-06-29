from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine, AsyncEngine
from src.config_schema import Config


async def create_database_engine(config: Config) -> AsyncEngine:
    database_url = (
        f"postgresql+psycopg://{config.database.user}:{config.database.password}"
        f"@{config.database.host}:{config.database.port}/{config.database.name}"
    )
    return create_async_engine(
        database_url,
        echo=config.debug,
        pool_pre_ping=True
    )


async def create_session_factory(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False
    )