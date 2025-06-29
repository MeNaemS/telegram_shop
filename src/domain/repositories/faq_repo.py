from typing import List
from abc import ABC, abstractmethod
from src.infrastructure.database.models.users import FAQ


class FAQRepositoryInterface(ABC):
    @abstractmethod
    async def get_faq_paginated(self, offset: int, limit: int) -> List[FAQ]:
        ...

    @abstractmethod
    async def get_total_faq_count(self) -> int:
        ...

    @abstractmethod
    async def get_faq_by_id(self, faq_id: int) -> FAQ | None:
        ...