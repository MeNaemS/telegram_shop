from typing import List
from src.domain.entities.category import Category
from src.domain.repositories.category_repo import CategoryRepositoryInterface
from src.application.dtos.main_menu import CategoryDTO
from src.application.mappers.main_menu_mapper import CategoryMapper


class GetCategoriesUseCase:
    def __init__(self, category_repo: CategoryRepositoryInterface, category_mapper: CategoryMapper):
        self.category_repo: CategoryRepositoryInterface = category_repo
        self.category_mapper: CategoryMapper = category_mapper

    async def execute(self, page: int = 0) -> CategoryDTO:
        offset: int = page * 9
        categories: List[Category] = await self.category_repo.get_categories_paginated(offset, 9)
        total: int = await self.category_repo.get_total_categories_count()
        return await self.category_mapper.to_category(
            {
                "items": categories,
                "current_page": page,
                "total_pages": (total + 8) // 9,
                "has_next": (page + 1) * 9 < total,
                "has_prev": page > 0
            }
        )
