from abc import ABC, abstractmethod
from typing import List
from src.infrastructure.database.models.orders import Cart, CartItem


class CartRepositoryInterface(ABC):
    @abstractmethod
    async def get_or_create_cart(self, user_id: int) -> Cart:
        ...

    @abstractmethod
    async def add_item_to_cart(self, user_id: int, product_id: int, quantity: int = 1) -> None:
        ...

    @abstractmethod
    async def get_cart_items(self, user_id: int) -> List[CartItem]:
        ...

    @abstractmethod
    async def remove_item_from_cart(self, user_id: int, cart_item_id: int) -> None:
        ...

    @abstractmethod
    async def clear_cart(self, user_id: int) -> None:
        ...
