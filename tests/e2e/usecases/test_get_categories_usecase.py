import pytest
from unittest.mock import AsyncMock
from src.application.usecases.get_categories import GetCategoriesUseCase
from src.domain.repositories.category_repo import CategoryRepositoryInterface
from src.application.mappers.main_menu_mapper import CategoryMapper
from src.domain.entities.category import Category


@pytest.mark.asyncio
async def test_get_categories_success():
    # Arrange
    mock_category_repo = AsyncMock(spec=CategoryRepositoryInterface)
    mock_category_mapper = AsyncMock(spec=CategoryMapper)
    
    categories = [
        Category(id=1, name="Electronics"),
        Category(id=2, name="Books")
    ]
    
    mock_category_repo.get_categories_paginated = AsyncMock(return_value=categories)
    mock_category_repo.get_total_categories_count = AsyncMock(return_value=2)
    
    expected_dto = AsyncMock()
    mock_category_mapper.to_category = AsyncMock(return_value=expected_dto)
    
    use_case = GetCategoriesUseCase(mock_category_repo, mock_category_mapper)
    
    # Act
    result = await use_case.execute(page=0)
    
    # Assert
    mock_category_repo.get_categories_paginated.assert_called_once_with(0, 9)
    mock_category_repo.get_total_categories_count.assert_called_once()
    mock_category_mapper.to_category.assert_called_once()
    
    call_args = mock_category_mapper.to_category.call_args[0][0]
    assert call_args["items"] == categories
    assert call_args["current_page"] == 0
    assert call_args["total_pages"] == 1
    assert call_args["has_next"] is False
    assert call_args["has_prev"] is False
    
    assert result == expected_dto


@pytest.mark.asyncio
async def test_get_categories_pagination():
    # Arrange
    mock_category_repo = AsyncMock(spec=CategoryRepositoryInterface)
    mock_category_mapper = AsyncMock(spec=CategoryMapper)
    
    categories = [Category(id=i, name=f"Category {i}") for i in range(1, 10)]
    
    mock_category_repo.get_categories_paginated = AsyncMock(return_value=categories)
    mock_category_repo.get_total_categories_count = AsyncMock(return_value=20)
    
    expected_dto = AsyncMock()
    mock_category_mapper.to_category = AsyncMock(return_value=expected_dto)
    
    use_case = GetCategoriesUseCase(mock_category_repo, mock_category_mapper)
    
    # Act
    result = await use_case.execute(page=1)
    
    # Assert
    mock_category_repo.get_categories_paginated.assert_called_once_with(9, 9)
    
    call_args = mock_category_mapper.to_category.call_args[0][0]
    assert call_args["current_page"] == 1
    assert call_args["total_pages"] == 3
    assert call_args["has_next"] is True
    assert call_args["has_prev"] is True