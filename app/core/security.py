from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
import jwt

from .config import settings


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Алгоритм шифрования, который мы будем использовать для токенов
ALGORITHM = "HS256"

# Время жизни токена по умолчанию
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7


def get_password_hash(password: str) -> str:
    """
    Превращает открытый пароль в нечитаемый хэш.
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Проверяет, совпадает ли введенный пароль с хэшем из базы данных.
    """
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """
    Генерирует JWT токен.
    В 'data' мы будем передавать словарь вида {"sub": str(user_id)}.
    """

    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=ALGORITHM)
    
    return encoded_jwt