from abc import ABC, abstractmethod
from typing import Optional


class ImageClientInterface(ABC):
    @abstractmethod
    async def get_image_url(self, image_path: Optional[str]) -> Optional[str]:
        ...

    @abstractmethod
    async def download_image(self, image_url: str) -> bytes:
        ...