from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.domain.repositories.cart_repo import CartRepositoryInterface
from src.infrastructure.database.models.orders import Cart, CartItem


class CartRepositoryImpl(CartRepositoryInterface):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_or_create_cart(self, user_id: int) -> Cart:
        result = await self.session.execute(
            select(Cart).where(Cart.user_id == user_id)
        )
        cart = result.scalar_one_or_none()
        
        if not cart:
            cart = Cart(user_id=user_id)
            self.session.add(cart)
            await self.session.commit()
            await self.session.refresh(cart)
        
        return cart

    async def add_item_to_cart(self, user_id: int, product_id: int, quantity: int = 1) -> None:
        cart = await self.get_or_create_cart(user_id)
        

        result = await self.session.execute(
            select(CartItem).where(
                CartItem.cart_id == cart.id,
                CartItem.product_id == product_id
            )
        )
        existing_item = result.scalar_one_or_none()
        
        if existing_item:
            existing_item.quantity += quantity
        else:
            cart_item = CartItem(
                cart_id=cart.id,
                product_id=product_id,
                quantity=quantity
            )
            self.session.add(cart_item)
        
        await self.session.commit()

    async def get_cart_items(self, user_id: int) -> List[CartItem]:
        from sqlalchemy.orm import selectinload
        result = await self.session.execute(
            select(CartItem)
            .join(Cart)
            .where(Cart.user_id == user_id)
            .options(selectinload(CartItem.product))
        )
        return result.scalars().all()

    async def remove_item_from_cart(self, user_id: int, cart_item_id: int) -> None:
        result = await self.session.execute(
            select(CartItem)
            .join(Cart)
            .where(Cart.user_id == user_id, CartItem.id == cart_item_id)
        )
        item = result.scalar_one_or_none()
        if item:
            await self.session.delete(item)
            await self.session.commit()

    async def clear_cart(self, user_id: int) -> None:
        from sqlalchemy import delete
        result = await self.session.execute(
            select(Cart).where(Cart.user_id == user_id)
        )
        cart = result.scalar_one_or_none()
        if cart:
            await self.session.execute(
                delete(CartItem).where(CartItem.cart_id == cart.id)
            )
            await self.session.commit()