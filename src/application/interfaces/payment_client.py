from abc import ABC, abstractmethod
from decimal import Decimal


class PaymentClientInterface(ABC):
    @abstractmethod
    async def create_payment(self, amount: Decimal, description: str, return_url: str) -> str:
        ...

    @abstractmethod
    async def check_payment_status(self, payment_id: str) -> bool:
        ...