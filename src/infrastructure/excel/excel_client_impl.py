from typing import List
from datetime import datetime
from pathlib import Path
import openpyxl
from openpyxl import Workbook
from src.application.interfaces.excel_client import ExcelClientInterface
from src.infrastructure.database.models.orders import CartItem


class ExcelClientImpl(ExcelClientInterface):
    def __init__(self, excel_path: str = "/app/reports/orders.xlsx"):
        self.excel_path = Path(excel_path)
        try:
            self.excel_path.parent.mkdir(parents=True, exist_ok=True)
        except (PermissionError, FileNotFoundError):
            pass

    async def write_order_to_excel(self, user_id: int, full_name: str, address: str, phone: str, payment_method: str, cart_items: List[CartItem]) -> None:
        if self.excel_path.exists():
            workbook = openpyxl.load_workbook(self.excel_path)
            worksheet = workbook.active
        else:
            workbook = Workbook()
            worksheet = workbook.active
            worksheet.title = "Orders"
            worksheet.append(["Дата", "ID пользователя", "ФИО", "Адрес", "Телефон", "Способ оплаты", "Товары", "Общая сумма"])

        total_amount = sum(item.product.price * item.quantity for item in cart_items)
        products_info = "; ".join([f"{item.product.name} x{item.quantity}" for item in cart_items])
        
        worksheet.append([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            user_id,
            full_name,
            address,
            phone,
            payment_method,
            products_info,
            float(total_amount)
        ])
        
        workbook.save(self.excel_path)