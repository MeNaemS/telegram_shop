from src.domain.repositories.cart_repo import CartRepositoryInterface


class AddToCartUseCase:
    def __init__(self, cart_repo: CartRepositoryInterface):
        self.cart_repo = cart_repo

    async def execute(self, user_id: int, product_id: int, quantity: int = 1) -> None:
        await self.cart_repo.add_item_to_cart(user_id, product_id, quantity)