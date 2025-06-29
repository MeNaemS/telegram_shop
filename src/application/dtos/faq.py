from dataclasses import dataclass
from typing import List
from src.infrastructure.database.models.users import FAQ


@dataclass(slots=True)
class FAQdto:
    items: List[FAQ]
    current_page: int
    total_pages: int
    has_next: bool
    has_prev: bool
