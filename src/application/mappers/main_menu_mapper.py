from src.application.dtos.main_menu import CategoryDTO


class CategoryMapper:
    @staticmethod
    async def to_category(data: dict) -> CategoryDTO:
        return CategoryDTO(**data)
