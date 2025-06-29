from src.domain.repositories.user_repo import UserRepositoryInterface


class RegisterUserUseCase:
    def __init__(self, user_repo: UserRepositoryInterface):
        self.user_repo = user_repo

    async def execute(self, user_id: int) -> None:
        existing_user = await self.user_repo.get_user(user_id)
        if not existing_user:
            await self.user_repo.create_user(user_id)