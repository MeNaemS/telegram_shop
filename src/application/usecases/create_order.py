from src.domain.repositories.cart_repo import CartRepositoryInterface
from src.domain.repositories.order_repo import OrderRepositoryInterface
from src.application.interfaces.excel_client import ExcelClientInterface


class CreateOrderUseCase:
    def __init__(self, cart_repo: CartRepositoryInterface, order_repo: OrderRepositoryInterface, excel_client: ExcelClientInterface):
        self.cart_repo = cart_repo
        self.order_repo = order_repo
        self.excel_client = excel_client

    async def execute(self, user_id: int, full_name: str, address: str, phone: str, payment_method: str) -> None:
        cart_items = await self.cart_repo.get_cart_items(user_id)
        if cart_items:
            await self.order_repo.create_order(user_id, full_name, address, phone, payment_method, cart_items)
            await self.excel_client.write_order_to_excel(user_id, full_name, address, phone, payment_method, cart_items)
            await self.cart_repo.clear_cart(user_id)