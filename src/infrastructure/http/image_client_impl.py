from typing import Optional
import aiohttp
from src.application.interfaces.image_client import ImageClientInterface
from src.config_schema import Config


class ImageClientImpl(ImageClientInterface):
    def __init__(self, config: Config):
        self.config = config
        self.base_url = "http://localhost:8000" if config.database.host == "localhost" else f"http://{config.database.host}:8000"

    async def get_image_url(self, image_path: Optional[str]) -> Optional[str]:
        if not image_path:
            return None
        return f"{self.base_url}/media/{image_path}"

    async def download_image(self, image_url: str) -> bytes:
        async with aiohttp.ClientSession() as session:
            async with session.get(image_url) as response:
                if response.status == 200:
                    return await response.read()
                return b""