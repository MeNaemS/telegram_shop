from decimal import Decimal
from typing import List
from src.domain.repositories.cart_repo import CartRepositoryInterface
from src.application.interfaces.payment_client import PaymentClientInterface
from src.infrastructure.database.models.orders import CartItem


class CreatePaymentUseCase:
    def __init__(self, cart_repo: CartRepositoryInterface, payment_client: PaymentClientInterface):
        self.cart_repo = cart_repo
        self.payment_client = payment_client

    async def execute(self, user_id: int) -> str:
        cart_items: List[CartItem] = await self.cart_repo.get_cart_items(user_id)
        if not cart_items:
            raise ValueError("Корзина пуста")
        
        total_amount = sum(item.product.price * item.quantity for item in cart_items)
        description = f"Заказ пользователя {user_id}"
        return_url = "https://t.me/your_bot"
        
        return await self.payment_client.create_payment(total_amount, description, return_url)