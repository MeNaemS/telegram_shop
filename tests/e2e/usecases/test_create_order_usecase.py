import pytest
from unittest.mock import AsyncMock
from src.application.usecases.create_order import CreateOrderUseCase
from src.domain.repositories.cart_repo import CartRepositoryInterface
from src.domain.repositories.order_repo import OrderRepositoryInterface
from src.application.interfaces.excel_client import ExcelClientInterface


@pytest.mark.asyncio
async def test_create_order_success(sample_cart_item):
    # Arrange
    mock_cart_repo = AsyncMock(spec=CartRepositoryInterface)
    mock_order_repo = AsyncMock(spec=OrderRepositoryInterface)
    mock_excel_client = AsyncMock(spec=ExcelClientInterface)
    
    mock_cart_repo.get_cart_items = AsyncMock(return_value=[sample_cart_item])
    mock_order_repo.create_order = AsyncMock()
    mock_excel_client.write_order_to_excel = AsyncMock()
    mock_cart_repo.clear_cart = AsyncMock()
    
    use_case = CreateOrderUseCase(mock_cart_repo, mock_order_repo, mock_excel_client)
    
    # Act
    await use_case.execute(12345, "John Doe", "123 Main St", "+1234567890", "Card")
    
    # Assert
    mock_cart_repo.get_cart_items.assert_called_once_with(12345)
    mock_order_repo.create_order.assert_called_once_with(
        12345, "John Doe", "123 Main St", "+1234567890", "Card", [sample_cart_item]
    )
    mock_excel_client.write_order_to_excel.assert_called_once_with(
        12345, "John Doe", "123 Main St", "+1234567890", "Card", [sample_cart_item]
    )
    mock_cart_repo.clear_cart.assert_called_once_with(12345)


@pytest.mark.asyncio
async def test_create_order_empty_cart():
    # Arrange
    mock_cart_repo = AsyncMock(spec=CartRepositoryInterface)
    mock_order_repo = AsyncMock(spec=OrderRepositoryInterface)
    mock_excel_client = AsyncMock(spec=ExcelClientInterface)
    
    mock_cart_repo.get_cart_items = AsyncMock(return_value=[])
    
    use_case = CreateOrderUseCase(mock_cart_repo, mock_order_repo, mock_excel_client)
    
    # Act
    await use_case.execute(12345, "John Doe", "123 Main St", "+1234567890", "Card")
    
    # Assert
    mock_cart_repo.get_cart_items.assert_called_once_with(12345)
    mock_order_repo.create_order.assert_not_called()
    mock_excel_client.write_order_to_excel.assert_not_called()
    mock_cart_repo.clear_cart.assert_not_called()