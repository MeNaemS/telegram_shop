from src.infrastructure.database.models.users import FAQ
from src.domain.repositories.faq_repo import FAQRepositoryInterface


class GetFAQByIdUseCase:
    def __init__(self, faq_repo: FAQRepositoryInterface):
        self.faq_repo = faq_repo

    async def execute(self, faq_id: int) -> FAQ | None:
        return await self.faq_repo.get_faq_by_id(faq_id)