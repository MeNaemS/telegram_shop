from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from src.domain.repositories.category_repo import CategoryRepositoryInterface
from src.infrastructure.database.models.products import Category as CategoryModel
from src.domain.entities.category import Category


class CategoryRepositoryImpl(CategoryRepositoryInterface):
    def __init__(self, session: AsyncSession):
        self.session: AsyncSession = session

    async def get_categories_paginated(self, offset: int, limit: int) -> List[Category]:
        result = await self.session.execute(
            select(CategoryModel).where(CategoryModel.parent_id.is_(None)).offset(offset).limit(limit)
        )
        models = result.scalars().all()
        return [Category(id=m.id, name=m.name, parent_id=m.parent_id) for m in models]

    async def get_subcatigory_paginated(
        self,
        parent_id: int,
        offset: int,
        limit: int
    ) -> List[Category]:
        result = await self.session.execute(
            select(CategoryModel).where(CategoryModel.parent_id == parent_id).offset(offset).limit(limit)
        )
        models = result.scalars().all()
        return [Category(id=m.id, name=m.name, parent_id=m.parent_id) for m in models]

    async def get_total_categories_count(self) -> int:
        result = await self.session.execute(
            select(func.count(CategoryModel.id)).where(CategoryModel.parent_id.is_(None))
        )
        return result.scalar_one() or 0

    async def get_total_subcategories_count(self, parent_id: int) -> int:
        result = await self.session.execute(
            select(func.count(CategoryModel.id)).where(CategoryModel.parent_id == parent_id)
        )
        return result.scalar_one() or 0
