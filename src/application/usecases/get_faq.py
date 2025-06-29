from typing import List
from src.infrastructure.database.models.users import FAQ
from src.domain.repositories.faq_repo import FAQRepositoryInterface
from src.application.dtos.faq import FAQdto


class GetFAQUseCase:
    def __init__(self, faq_repo: FAQRepositoryInterface):
        self.faq_repo = faq_repo

    async def execute(self, page: int = 0) -> FAQdto:
        offset = page * 4
        faqs: List[FAQ] = await self.faq_repo.get_faq_paginated(offset, 4)
        total = await self.faq_repo.get_total_faq_count()
        return FAQdto(
            items=faqs,
            current_page=page,
            total_pages=(total + 3) // 4,
            has_next=(page + 1) * 4 < total,
            has_prev=page > 0
        )