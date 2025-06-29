from dataclasses import dataclass
from decimal import Decimal
from typing import Optional


@dataclass
class Product:
    id: int
    name: str
    description: Optional[str]
    image: Optional[str]
    price: Decimal
    category_id: int