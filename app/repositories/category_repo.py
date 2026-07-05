from sqlmodel import select, col
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Sequence


from ..models.category import Category
from ..schemas.category import CategoryCreate


class CategoryRepository:
    """
    Слой доступа к данным для сущности User.
    Изолирует написание SQL-запросов от остальной бизнес-логики приложения.
    """
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, category_id: int) -> Category | None:
        """
        Ищет категорию по ID.
        Возвращает объект Category или None, если такой категории нет.
        """
        statement = select(Category).where(Category.id == category_id)
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()

    async def search_by_header(self, search_query: str) -> Sequence[Category]:
        """
        Ищет категорию по заголовку.
        """
        statement = select(Category).where(col(Category.header).ilike(f"%{search_query}%"))
        result = await self.session.execute(statement)
        return result.scalars().all()
    
    async def get_active_categories(self) -> Sequence[Category]:
        """
        Возвращает список всех активных категорий.
        Это понадобится для выпадающего списка при создании тикета на фронтенде.
        """
        statement = select(Category).where(Category.is_active)
        result = await self.session.execute(statement)
        return result.scalars().all()

    async def create(self, category_in: CategoryCreate) -> Category:
        """
        Создает новую категорию в базе данных.
        """
        db_category = Category(**category_in.model_dump())
        
        self.session.add(db_category)
        await self.session.flush() 
        await self.session.refresh(db_category)
        
        return db_category

    async def update(self, db_category: Category, update_data: dict) -> Category:
        """
        Обновляет существующую категорию.
        Принимает объект из БД и словарь с новыми данными.
        """
        for key, value in update_data.items():
            setattr(db_category, key, value)
            
        self.session.add(db_category)
        await self.session.flush()
        await self.session.refresh(db_category)
        
        return db_category