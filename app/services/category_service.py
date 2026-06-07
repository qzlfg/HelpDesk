from typing import Sequence

from ..models.category import Category
from ..schemas.category import CategoryCreate, CategoryUpdate
from ..repositories.category_repo import CategoryRepository


class CategoryService:
    """
    Слой бизнес-логики для управления категориями тикетов.
    Обеспечивает создание, поиск и безопасное обновление категорий.
    """
    def __init__(self, category_repo: CategoryRepository) -> None:
        self.category_repo = category_repo
    
    
    async def create_category(self, category_in: CategoryCreate) -> Category:
        return await self.category_repo.create(category_in)
    
    
    async def get_category_by_id(self, id: int) -> Category:
        """
        Ищет категорию по ID. Если категория не найдена, выбрасывает ошибку (404).
        """
        res = await self.category_repo.get_by_id(id)
        
        if not res:
            raise ValueError("Не существует данной категории")

        return res


    async def get_active_categories(self) -> Sequence[Category]:
        return await self.category_repo.get_active_categories()
    
    
    async def search_by_header(self, header: str) -> Sequence[Category]:
        """
        Поиск категорий по названию (заголовку).
        Пустой список в ответе означает, что совпадений нет.
        """
        return await self.category_repo.search_by_header(header)


    async def update_category(self, category_id: int, update_in: CategoryUpdate) -> Category:
        update_data = update_in.model_dump(exclude_unset=True)
        category_db = await self.get_category_by_id(category_id)
        
        return await self.category_repo.update(category_db, update_data)