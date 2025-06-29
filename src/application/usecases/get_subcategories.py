from typing import List
from src.domain.entities.category import Category
from src.domain.repositories.category_repo import CategoryRepositoryInterface
from src.application.dtos.main_menu import CategoryDTO
from src.application.mappers.main_menu_mapper import CategoryMapper


class GetSubcategoriesUseCase:
    def __init__(self, category_repo: CategoryRepositoryInterface, category_mapper: CategoryMapper):
        self.category_repo: CategoryRepositoryInterface = category_repo
        self.category_mapper: CategoryMapper = category_mapper

    async def execute(self, parent_id: int, page: int = 0) -> CategoryDTO:
        offset: int = page * 9
        categories: List[Category] = await self.category_repo.get_subcatigory_paginated(parent_id, offset, 9)
        total: int = await self.category_repo.get_total_subcategories_count(parent_id)
        return await self.category_mapper.to_category(
            {
                "items": categories,
                "current_page": page,
                "total_pages": (total + 8) // 9,
                "has_next": (page + 1) * 9 < total,
                "has_prev": page > 0
            }
        )