import pytest
from unittest.mock import AsyncMock
from src.application.usecases.get_cart import GetCartUseCase
from src.application.usecases.add_to_cart import AddToCartUseCase


@pytest.mark.asyncio
async def test_get_cart_use_case_empty():
    # Arrange
    mock_cart_repo = AsyncMock()
    mock_cart_repo.get_cart_items = AsyncMock(return_value=[])
    
    use_case = GetCartUseCase(mock_cart_repo)
    
    # Act
    result = await use_case.execute(12345)
    
    # Assert
    mock_cart_repo.get_cart_items.assert_called_once_with(12345)
    assert result == []


@pytest.mark.asyncio
async def test_get_cart_use_case_with_items(sample_cart_item):
    # Arrange
    mock_cart_repo = AsyncMock()
    mock_cart_repo.get_cart_items = AsyncMock(return_value=[sample_cart_item])
    
    use_case = GetCartUseCase(mock_cart_repo)
    
    # Act
    result = await use_case.execute(12345)
    
    # Assert
    mock_cart_repo.get_cart_items.assert_called_once_with(12345)
    assert result == [sample_cart_item]


@pytest.mark.asyncio
async def test_add_to_cart_use_case():
    # Arrange
    mock_cart_repo = AsyncMock()
    mock_cart_repo.add_item_to_cart = AsyncMock()
    
    use_case = AddToCartUseCase(mock_cart_repo)
    
    # Act
    await use_case.execute(12345, 123, 2)
    
    # Assert
    mock_cart_repo.add_item_to_cart.assert_called_once_with(12345, 123, 2)