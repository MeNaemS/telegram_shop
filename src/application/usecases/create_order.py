from src.domain.repositories.cart_repo import CartRepositoryInterface
from src.domain.repositories.order_repo import OrderRepositoryInterface
from src.application.interfaces.excel_client import ExcelClientInterface
from src.application.interfaces.payment_client import PaymentClientInterface


class CreateOrderUseCase:
    def __init__(self, cart_repo: CartRepositoryInterface, order_repo: OrderRepositoryInterface, excel_client: ExcelClientInterface, payment_client: PaymentClientInterface):
        self.cart_repo = cart_repo
        self.order_repo = order_repo
        self.excel_client = excel_client
        self.payment_client = payment_client

    async def execute(self, user_id: int, full_name: str, address: str, phone: str, payment_id: str) -> None:
        is_paid = await self.payment_client.check_payment_status(payment_id)
        if not is_paid:
            raise ValueError("Платеж не подтвержден")
            
        cart_items = await self.cart_repo.get_cart_items(user_id)
        if cart_items:
            await self.order_repo.create_order(user_id, full_name, address, phone, "YooKassa", cart_items)
            await self.excel_client.write_order_to_excel(user_id, full_name, address, phone, "YooKassa", cart_items)
            await self.cart_repo.clear_cart(user_id)