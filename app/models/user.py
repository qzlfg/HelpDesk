from __future__ import annotations
from typing import TYPE_CHECKING, List

from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, Enum
from .enums import Role

if TYPE_CHECKING:
    from app.models.ticket import Ticket
    from .comment import Comment
    from .attachment import Attachment
    from .ticket_history import TicketHistory


class User(SQLModel, table=True):
    """
    Модель учетной записи пользователя системы.
    Содержит данные для аутентификации и связи с тикетами, к которым причастен пользователь 
    (либо как создатель, либо как исполнитель(агент)).
    """
    id: int | None = Field(default=None, primary_key=True, index=True)
    email: str = Field(unique=True, index=True, max_length=255)
    password_hash: str = Field(max_length=255)
    role: Role = Field(sa_column=Column(Enum(Role, name="user_role_enum"), nullable=False, server_default=Role.CLIENT.value))
    
    # Список тикетов, которые этот пользователь создал (клиент)
    created_tickets: List[Ticket] = Relationship(back_populates="creator")
    
    # Список тикетов, которые назначены на этого пользователя для решения (агент)
    assigned_tickets: List[Ticket] = Relationship(back_populates="assignee")
    
    comment_tickets: List[Comment] = Relationship(back_populates="creator_of_comment")
    created_attachments: List[Attachment] = Relationship(back_populates="user")
    changed_tickets: List[TicketHistory] = Relationship(back_populates="user_changed")