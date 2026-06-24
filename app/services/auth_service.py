from ..repositories.user_repo import UserRepository
from ..core import security


class AuthService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo
        
    
    
    async def authenticate_user(self, email: str, password: str) -> str:
        """
        Проверяет логин/пароль и возвращает готовый JWT-токен.
        """
        user = await self.user_repo.get_by_email(email)
        
        if not user:
            raise ValueError("Неверный email или пароль")
        
        if not security.verify_password(password, user.password_hash):
            raise ValueError("Неверный email или пароль")
        
        token_data = {"sub": str(user.id)}
        
        return security.create_access_token(data=token_data)