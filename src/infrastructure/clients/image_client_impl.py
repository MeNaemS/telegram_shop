from typing import Optional
from pathlib import Path
from src.application.interfaces.image_client import ImageClientInterface


class ImageClientImpl(ImageClientInterface):
    def __init__(self):
        self.media_path = Path("/app/media")

    async def get_image_path(self, image_name: Optional[str]) -> Optional[Path]:
        if not image_name:
            return None
        image_path = self.media_path / image_name
        return image_path if image_path.exists() else None