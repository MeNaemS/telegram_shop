from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from src.domain.repositories.order_repo import OrderRepositoryInterface
from src.infrastructure.database.models.orders import Order, OrderItem, CartItem


class OrderRepositoryImpl(OrderRepositoryInterface):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_order(self, user_id: int, full_name: str, address: str, phone: str, payment_method: str, cart_items: List[CartItem]) -> None:
        order = Order(
            user_id=user_id,
            full_name=full_name,
            address=address,
            phone=phone,
            payment_method=payment_method
        )
        self.session.add(order)
        await self.session.flush()
        
        for cart_item in cart_items:
            order_item = OrderItem(
                order_id=order.id,
                product_id=cart_item.product_id,
                quantity=cart_item.quantity,
                price=cart_item.product.price
            )
            self.session.add(order_item)
        
        await self.session.commit()