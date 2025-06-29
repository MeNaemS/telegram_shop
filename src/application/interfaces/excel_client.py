from abc import ABC, abstractmethod
from typing import List
from src.infrastructure.database.models.orders import CartItem


class ExcelClientInterface(ABC):
    @abstractmethod
    async def write_order_to_excel(self, user_id: int, full_name: str, address: str, phone: str, payment_method: str, cart_items: List[CartItem]) -> None:
        ...