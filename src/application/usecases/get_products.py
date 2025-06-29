from typing import List
from src.domain.entities.product import Product
from src.domain.repositories.product_repo import ProductRepositoryInterface


class GetProductsUseCase:
    def __init__(self, product_repo: ProductRepositoryInterface):
        self.product_repo = product_repo

    async def execute(self, category_id: int) -> List[Product]:
        return await self.product_repo.get_products_by_category(category_id)