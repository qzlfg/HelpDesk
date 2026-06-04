from sqlmodel import select, col
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Sequence

from ..models.comment import Comment
from ..schemas.comment import CommentCreate

class CommentRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def get_by_id(self, comment_id: int) -> Comment | None:
        """
        Ищет конкретный комментарий по его уникальному ID.
        """
        statement = select(Comment).where(Comment.id == comment_id)
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()
    
    async def get_by_ticket_id(self, ticket_id: int) -> Sequence[Comment]:
        """
        Получает все комментарии для конкретного тикета.
        Метод для отрисовки "чата" внутри заявки.
        """
        statement = (
            select(Comment)
            .where(Comment.ticket_id == ticket_id)
            .order_by(col(Comment.created_at))
        )
        result = await self.session.execute(statement)
        return result.scalars().all()

    async def create(self, comment_in: CommentCreate, creator_id: int) -> Comment:
        """
        Создает новый комментарий.
        ID автора (creator_id) внедряется на сервере для безопасности, 
        чтобы нельзя было подделать авторство сообщения.
        """
        comment_data = comment_in.model_dump()
        comment_data["creator_id"] = creator_id
        
        db_comment = Comment(**comment_data)
        
        self.session.add(comment_data)
        await self.session.flush() 
        await self.session.refresh(comment_data)
        
        return db_comment

    async def update(self, db_comment: Comment, update_data: dict) -> Comment:
        for key, value in update_data.items():
            setattr(db_comment, key, value)
        
        self.session.add(db_comment)
        await self.session.flush()
        await self.session.refresh(db_comment)
        
        return db_comment