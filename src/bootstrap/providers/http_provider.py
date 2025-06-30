from typing import AsyncIterable
from dishka import Provider, provide, Scope
import aiohttp
from src.config_schema import Config


class HttpProvider(Provider):
    @provide(scope=Scope.APP)
    async def get_http_session(self, config: Config) -> AsyncIterable[aiohttp.ClientSession]:
        timeout = aiohttp.ClientTimeout(total=config.http.timeout)
        connector = aiohttp.TCPConnector(limit=config.http.connector_limit)
        
        async with aiohttp.ClientSession(
            timeout=timeout,
            connector=connector
        ) as session:
            yield session