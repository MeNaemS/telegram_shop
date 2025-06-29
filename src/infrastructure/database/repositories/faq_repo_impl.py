from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from src.domain.repositories.faq_repo import FAQRepositoryInterface
from src.infrastructure.database.models.users import FAQ


class FAQRepositoryImpl(FAQRepositoryInterface):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_faq_paginated(self, offset: int, limit: int) -> List[FAQ]:
        result = await self.session.execute(
            select(FAQ).offset(offset).limit(limit)
        )
        return result.scalars().all()

    async def get_total_faq_count(self) -> int:
        result = await self.session.execute(select(func.count(FAQ.id)))
        return result.scalar_one() or 0

    async def get_faq_by_id(self, faq_id: int) -> FAQ | None:
        result = await self.session.execute(select(FAQ).where(FAQ.id == faq_id))
        return result.scalar_one_or_none()