from ..models.user import User
from ..schemas.user import UserCreate, UserUpdate, UserUpdateAdmin
from ..repositories.user_repo import UserRepository
from ..models.enums import Role
from ..core.security import get_password_hash

class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo
        
    async def create_user(self, user_in: UserCreate) -> User:
        '''
        Регистрирует нового пользователя.
        Проверяет уникальность email и безопасно хеширует пароль перед сохранением в БД.
        '''
        existing_user = await self.user_repo.get_by_email(user_in.email)    
        if existing_user:
            raise ValueError(f"Пользователь с email {user_in.email} уже существует")

        hashed_password = get_password_hash(user_in.password)
        user_data = user_in.model_dump()
        user_data["password"] = hashed_password
        user_data["role"] = Role.CLIENT

        return await self.user_repo.create(user_data)

    async def get_user_by_id(self, id: int) -> User:
        """
        Возвращает пользователя по ID или выбрасывает ошибку.
        """
        res = await self.user_repo.get_by_id(id)
        if not res:
            raise ValueError("Такого пользователя не существует")
        return res
        
    async def get_user_by_email(self, email: str) -> User:
        """
        Возвращает пользователя по почте или выбрасывает ошибку.
        """
        res = await self.user_repo.get_by_email(email)
        if not res:
            raise ValueError(f"Пользователь с email {email} не найден")
        return res
        
    
    async def update_user(self, user_id: int, update_in: UserUpdate) -> User:
        user_db = await self.get_user_by_id(user_id)
        
        update_data = update_in.model_dump(exclude_unset=True)
        
        if "password" in update_data:
            update_data["password"] = get_password_hash(update_data["password"])
            
        return await self.user_repo.update(user_db, update_data)
    
    async def update_user_by_admin(self, user_id: int, update_in: UserUpdateAdmin) -> User:
        user_db = await self.get_user_by_id(user_id)
        
        update_data = update_in.model_dump(exclude_unset=True)
        
        if "password" in update_data:
            update_data["password"] = get_password_hash(update_data["password"])
            
        return await self.user_repo.update(user_db, update_data)