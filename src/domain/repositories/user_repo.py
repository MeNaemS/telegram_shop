from abc import ABC, abstractmethod
from src.infrastructure.database.models.users import UserSubscription


class UserRepositoryInterface(ABC):
    @abstractmethod
    async def create_user(self, user_id: int) -> UserSubscription:
        ...

    @abstractmethod
    async def get_user(self, user_id: int) -> UserSubscription | None:
        ...