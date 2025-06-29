from abc import ABC, abstractmethod
from typing import List
from src.domain.entities.category import Category


class CategoryRepositoryInterface(ABC):
    @abstractmethod
    async def get_categories_paginated(
        self,
        offset: int,
        limit: int
    ) -> List[Category]:
        ...

    @abstractmethod
    async def get_subcatigory_paginated(
        self,
        parent_id: int,
        offset: int,
        limit: int
    ) -> List[Category]:
        ...

    @abstractmethod
    async def get_total_categories_count(self) -> int:
        ...

    @abstractmethod
    async def get_total_subcategories_count(self, parent_id: int) -> int:
        ...
