from aiogram.types import CallbackQuery, InlineKeyboardMarkup, FSInputFile
from src.application.interfaces.image_client import ImageClientInterface
from src.domain.entities.product import Product


class ProductService:
    def __init__(self, image_client: ImageClientInterface):
        self.image_client = image_client

    async def send_product_with_image(
        self, 
        callback: CallbackQuery, 
        product: Product, 
        text: str, 
        keyboard: InlineKeyboardMarkup
    ) -> bool:
        if product.image:
            image_path = await self.image_client.get_image_path(product.image)
            if image_path and image_path.exists():
                try:
                    photo = FSInputFile(image_path)
                    await callback.message.delete()
                    await callback.bot.send_photo(
                        chat_id=callback.message.chat.id,
                        photo=photo,
                        caption=text,
                        reply_markup=keyboard
                    )
                    return True
                except Exception:
                    pass
        return False