from src.domain.repositories.cart_repo import CartRepositoryInterface


class RemoveFromCartUseCase:
    def __init__(self, cart_repo: CartRepositoryInterface):
        self.cart_repo = cart_repo

    async def execute(self, user_id: int, cart_item_id: int) -> None:
        await self.cart_repo.remove_item_from_cart(user_id, cart_item_id)