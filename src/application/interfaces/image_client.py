from abc import ABC, abstractmethod
from typing import Optional
from pathlib import Path


class ImageClientInterface(ABC):
    @abstractmethod
    async def get_image_path(self, image_name: Optional[str]) -> Optional[Path]:
        ...