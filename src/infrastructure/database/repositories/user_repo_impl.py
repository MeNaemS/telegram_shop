from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.domain.repositories.user_repo import UserRepositoryInterface
from src.infrastructure.database.models.users import UserSubscription


class UserRepositoryImpl(UserRepositoryInterface):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_user(self, user_id: int) -> UserSubscription:
        user = UserSubscription(user_id=user_id, is_subscribed=False)
        self.session.add(user)
        await self.session.commit()
        return user

    async def get_user(self, user_id: int) -> UserSubscription | None:
        result = await self.session.execute(
            select(UserSubscription).where(UserSubscription.user_id == user_id)
        )
        return result.scalar_one_or_none()