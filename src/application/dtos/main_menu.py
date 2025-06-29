from dataclasses import dataclass
from typing import List
from src.domain.entities.category import Category


@dataclass(slots=True)
class CategoryDTO:
    items: List[Category]
    current_page: int
    total_pages: int
    has_next: bool
    has_prev: bool
