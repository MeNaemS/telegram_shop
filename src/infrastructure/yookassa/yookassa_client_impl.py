import aiohttp
import base64
from decimal import Decimal
from uuid import uuid4
from src.application.interfaces.payment_client import PaymentClientInterface
from src.config_schema import Config


class YooKassaClientImpl(PaymentClientInterface):
    def __init__(self, config: Config, session: aiohttp.ClientSession):
        self.shop_id = config.yookassa.shop_id
        self.secret_key = config.yookassa.secret_key
        self.base_url = "https://api.yookassa.ru/v3"
        self.session = session

    async def create_payment(self, amount: Decimal, description: str, return_url: str) -> str:
        auth = base64.b64encode(f"{self.shop_id}:{self.secret_key}".encode()).decode()
        
        payload = {
            "amount": {
                "value": str(amount),
                "currency": "RUB"
            },
            "confirmation": {
                "type": "redirect",
                "return_url": return_url
            },
            "description": description
        }
        
        headers = {
            "Authorization": f"Basic {auth}",
            "Content-Type": "application/json",
            "Idempotence-Key": str(uuid4())
        }
        
        async with self.session.post(
            f"{self.base_url}/payments",
            json=payload,
            headers=headers
        ) as response:
            data = await response.json()
            return data["confirmation"]["confirmation_url"]

    async def check_payment_status(self, payment_id: str) -> bool:
        auth = base64.b64encode(f"{self.shop_id}:{self.secret_key}".encode()).decode()
        
        headers = {
            "Authorization": f"Basic {auth}",
            "Content-Type": "application/json"
        }
        
        async with self.session.get(
            f"{self.base_url}/payments/{payment_id}",
            headers=headers
        ) as response:
            data = await response.json()
            return data.get("status") == "succeeded"