from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.user import User


class UserRepository:
    """
    Слой доступа к данным для сущности User.
    Изолирует написание SQL-запросов от остальной бизнес-логики приложения.
    """
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, user_id: int) -> User | None:
        """
        Ищет пользователя по ID.
        Возвращает объект User или None, если такого пользователя нет.
        """
        statement = select(User).where(User.id == user_id)
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()

    async def get_by_email(self, email: str) -> User | None:
        """
        Ищет пользователя по email (полезно для логина и проверки уникальности).
        """
        statement = select(User).where(User.email == email)
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()

    async def create(self, user_in: dict) -> User:
        """
        Создает нового пользователя в базе данных.
        
        Принимает словарь (dict), а не Pydantic-схему, так как ожидает уже 
        полностью подготовленные данные от слоя сервисов (с захешированным паролем и назначенной ролью).
        """
        db_user = User(**user_in)
        
        self.session.add(db_user)
        # flush() отправляет SQL-запрос INSERT в базу, база генерирует ID,
        # но изменения еще не зафиксированы окончательно (можно сделать rollback)
        await self.session.flush() 
        await self.session.refresh(db_user)
        
        return db_user

    async def update(self, db_user: User, update_data: dict) -> User:
        """
        Обновляет существующего пользователя.
        Принимает объект из БД и словарь с новыми данными.
        """
        for key, value in update_data.items():
            setattr(db_user, key, value)
            
        self.session.add(db_user)
        await self.session.flush()
        await self.session.refresh(db_user)
        
        return db_user