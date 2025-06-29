from typing import List
from src.infrastructure.database.models.orders import CartItem
from src.domain.repositories.cart_repo import CartRepositoryInterface


class GetCartUseCase:
    def __init__(self, cart_repo: CartRepositoryInterface):
        self.cart_repo = cart_repo

    async def execute(self, user_id: int) -> List[CartItem]:
        return await self.cart_repo.get_cart_items(user_id)