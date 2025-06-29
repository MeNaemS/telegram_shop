from abc import ABC, abstractmethod
from typing import List
from src.domain.entities.product import Product


class ProductRepositoryInterface(ABC):
    @abstractmethod
    async def get_products_by_category(self, category_id: int) -> List[Product]:
        ...

    @abstractmethod
    async def get_product_by_id(self, product_id: int) -> Product | None:
        ...