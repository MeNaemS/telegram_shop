import pytest
from unittest.mock import AsyncMock
from src.application.usecases.register_user import RegisterUserUseCase


@pytest.mark.asyncio
async def test_register_user_use_case_new_user():
    # Arrange
    mock_user_repo = AsyncMock()
    mock_user_repo.get_user = AsyncMock(return_value=None)
    mock_user_repo.create_user = AsyncMock()
    
    use_case = RegisterUserUseCase(mock_user_repo)
    
    # Act
    await use_case.execute(12345)
    
    # Assert
    mock_user_repo.get_user.assert_called_once_with(12345)
    mock_user_repo.create_user.assert_called_once_with(12345)


@pytest.mark.asyncio
async def test_register_user_use_case_existing_user(sample_user):
    # Arrange
    mock_user_repo = AsyncMock()
    mock_user_repo.get_user = AsyncMock(return_value=sample_user)
    mock_user_repo.create_user = AsyncMock()
    
    use_case = RegisterUserUseCase(mock_user_repo)
    
    # Act
    await use_case.execute(12345)
    
    # Assert
    mock_user_repo.get_user.assert_called_once_with(12345)
    mock_user_repo.create_user.assert_not_called()


@pytest.mark.asyncio
async def test_telegram_subscription_use_case():
    # Arrange
    mock_telegram_client = AsyncMock()
    mock_telegram_client.check_chat_member = AsyncMock(return_value=True)
    
    from src.application.usecases.telegram_subscription import TelegramSubscriptionUseCase
    use_case = TelegramSubscriptionUseCase(mock_telegram_client)
    
    # Act
    result = await use_case.check_user_subscription(12345)
    
    # Assert
    mock_telegram_client.check_chat_member.assert_called_once_with(user_id=12345)
    assert result is True