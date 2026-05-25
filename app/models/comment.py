from __future__ import annotations
from typing import TYPE_CHECKING, List

from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime, timezone


if TYPE_CHECKING:
    from .user import User
    from .ticket import Ticket
    from .attachment import Attachment
    
class Comment(SQLModel, table=True):
    """
    Модель комментария к тикету.
    Хранит историю переписки по заявке. Может содержать как публичные ответы 
    для клиента, так и внутренние заметки (is_internal) только для сотрудников.
    """
    id: int | None = Field(default=None, primary_key=True, index=True)
    content: str = Field(nullable=False)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    #Внешние ключи
    creator_id: int = Field(foreign_key="user.id", index=True)
    ticket_id: int = Field(foreign_key="ticket.id", index=True)
    
    # Флаг «только для агентов». Если True — при выдаче через API клиентам 
    # мы будем отфильтровывать этот комментарий.
    is_internal: bool = Field(default=False, nullable=False)
    
    #Связи
    creator_of_comment: User = Relationship(back_populates="comment_tickets")
    ticket: Ticket = Relationship(back_populates="comments")
    attachments_with_comment: List[Attachment] = Relationship(back_populates="comment")