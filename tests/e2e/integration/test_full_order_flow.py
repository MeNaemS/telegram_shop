import pytest
from unittest.mock import AsyncMock, MagicMock
from src.application.usecases.create_order import CreateOrderUseCase
from src.infrastructure.database.repositories.cart_repo_impl import CartRepositoryImpl
from src.infrastructure.database.repositories.order_repo_impl import OrderRepositoryImpl
from src.infrastructure.excel.excel_client_impl import ExcelClientImpl
from pathlib import Path
from tempfile import TemporaryDirectory


@pytest.mark.asyncio
async def test_full_order_creation_flow(mock_session, sample_cart_item):
    # Arrange
    with TemporaryDirectory() as temp_dir:
        # Setup repositories with mocked session
        cart_repo = CartRepositoryImpl(mock_session)
        order_repo = OrderRepositoryImpl(mock_session)
        
        # Setup Excel client with temp directory
        excel_client = ExcelClientImpl(str(Path(temp_dir) / "test_orders.xlsx"))
        
        # Mock cart repo to return cart items
        cart_repo.get_cart_items = AsyncMock(return_value=[sample_cart_item])
        cart_repo.clear_cart = AsyncMock()
        
        # Mock order repo
        order_repo.create_order = AsyncMock()
        
        # Create use case
        use_case = CreateOrderUseCase(cart_repo, order_repo, excel_client)
        
        # Act
        await use_case.execute(
            user_id=12345,
            full_name="John Doe",
            address="123 Main St",
            phone="+1234567890",
            payment_method="Card"
        )
        
        # Assert
        # Verify database operations
        cart_repo.get_cart_items.assert_called_once_with(12345)
        order_repo.create_order.assert_called_once()
        cart_repo.clear_cart.assert_called_once_with(12345)
        
        # Verify Excel file was created
        assert excel_client.excel_path.exists()
        
        # Verify Excel content
        import openpyxl
        workbook = openpyxl.load_workbook(excel_client.excel_path)
        worksheet = workbook.active
        
        data_row = [cell.value for cell in worksheet[2]]
        assert data_row[1] == 12345
        assert data_row[2] == "John Doe"
        assert data_row[5] == "Card"


@pytest.mark.asyncio
async def test_order_flow_with_empty_cart(mock_session):
    # Arrange
    with TemporaryDirectory() as temp_dir:
        cart_repo = CartRepositoryImpl(mock_session)
        order_repo = OrderRepositoryImpl(mock_session)
        excel_client = ExcelClientImpl(str(Path(temp_dir) / "test_orders.xlsx"))
        
        # Mock empty cart
        cart_repo.get_cart_items = AsyncMock(return_value=[])
        
        use_case = CreateOrderUseCase(cart_repo, order_repo, excel_client)
        
        # Act
        await use_case.execute(
            user_id=12345,
            full_name="John Doe",
            address="123 Main St",
            phone="+1234567890",
            payment_method="Card"
        )
        
        # Assert
        cart_repo.get_cart_items.assert_called_once_with(12345)
        # Should not create order or Excel entry for empty cart
        assert not excel_client.excel_path.exists()