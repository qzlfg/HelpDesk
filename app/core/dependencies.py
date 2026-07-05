from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
import jwt


from app.core.config import settings
from app.core.database import get_async_session
from app.core.security import ALGORITHM

from app.repositories.user_repo import UserRepository
from app.repositories.category_repo import CategoryRepository

from app.services.auth_service import AuthService
from app.services.user_service import UserService
from app.services.category_service import CategoryService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def get_user_repo(session: AsyncSession = Depends(get_async_session)) -> UserRepository:
    return UserRepository(session)

def get_category_repo(session: AsyncSession = Depends(get_async_session)) -> CategoryRepository:
    return CategoryRepository(session)

def get_auth_service(user_repo: UserRepository = Depends(get_user_repo)) -> AuthService:
    return AuthService(user_repo)

def get_category_service(category_repo: CategoryRepository = Depends(get_category_repo)) -> CategoryService:
    return CategoryService(category_repo)

def get_user_service(user_repo: UserRepository = Depends(get_user_repo)) -> UserService:
    return UserService(user_repo)


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    user_service: UserService = Depends(get_user_service)
):
    """
    Расшифровывает JWT-токен, достает ID пользователя и проверяет его в БД.
    Возвращает объект пользователя или выбрасывает ошибку 401.
    """
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Не удалось проверить учетные данные (неверный или просроченный токен)",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(
            token, 
            settings.secret_key, 
            algorithms=[ALGORITHM]
        )
        
        user_id_str: str | None = payload.get("sub", None)
        if user_id_str is None:
            raise credentials_exception
        
        user_id = int(user_id_str) 
        
    except (jwt.InvalidTokenError, ValueError):
        raise credentials_exception
        
    user = await user_service.get_user_by_id(user_id)
        
    return user