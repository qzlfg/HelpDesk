import os
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from typing import AsyncGenerator


#Получаем URL базы данных из переменных окружения.
# На этапе настройки проекта можно использовать os.getenv. 
# Позже это лучше перенести в pydantic-settings (файл config.py).
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql+asyncpg://admin:helpdesk_secret_password@localhost:5432/helpdesk_db"
)

engine = create_async_engine(DATABASE_URL, echo=True)

async_session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session