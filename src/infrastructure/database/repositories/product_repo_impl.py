from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.domain.repositories.product_repo import ProductRepositoryInterface
from src.infrastructure.database.models.products import Product as ProductModel
from src.domain.entities.product import Product


class ProductRepositoryImpl(ProductRepositoryInterface):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_products_by_category(self, category_id: int) -> List[Product]:
        result = await self.session.execute(
            select(ProductModel).where(ProductModel.category_id == category_id)
        )
        models = result.scalars().all()
        return [Product(id=m.id, name=m.name, description=m.description, image=m.image, price=m.price, category_id=m.category_id) for m in models]

    async def get_product_by_id(self, product_id: int) -> Product | None:
        result = await self.session.execute(
            select(ProductModel).where(ProductModel.id == product_id)
        )
        model = result.scalar_one_or_none()
        return Product(id=model.id, name=model.name, description=model.description, image=model.image, price=model.price, category_id=model.category_id) if model else None