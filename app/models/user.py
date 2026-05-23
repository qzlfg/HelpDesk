from __future__ import annotations
from typing import TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, Enum
from enum import Enum as PyEnum

if TYPE_CHECKING:
    from app.models.ticket import Ticket
class Role(str, PyEnum):
    """
    Роли пользователей для контроля доступа (RBAC).
    Определяют, какие эндпоинты и действия доступны пользователю:
    - CLIENT: может создавать тикеты и видеть только свои.
    - AGENT: обрабатывает тикеты, видит все заявки, пишет внутренние комментарии.
    - ADMIN: управляет системой (настраивает категории, SLA, блокирует юзеров).
    """
    CLIENT = "client"
    AGENT = "agent"
    ADMIN = "admin"


class User(SQLModel, table=True):
    """
    Модель учетной записи пользователя системы.
    Содержит данные для аутентификации и связи с тикетами, к которым причастен пользователь 
    (либо как создатель, либо как исполнитель(агент)).
    """
    id: int | None = Field(default=None, primary_key=True, index=True)
    email: str = Field(unique=True, index=True, max_length=255)
    password_hash: str = Field(max_length=255)
    role: Role = Field(sa_column=Column(Enum(Role), nullable=False, server_default=Role.CLIENT.value))
    
    # Список тикетов, которые этот пользователь создал (клиент)
    created_tickets: list[Ticket] = Relationship(back_populates="creator")
    # Список тикетов, которые назначены на этого пользователя для решения (агент)
    assigned_tickets: list[Ticket] = Relationship(back_populates="assignee")