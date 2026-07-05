from __future__ import annotations
from typing import TYPE_CHECKING, List

from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, Enum
from datetime import datetime, timezone

from .enums import Priority, Status

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.category import Category
    from .comment import Comment
    from .attachment import Attachment
    from .ticket_history import TicketHistory
    

class Ticket(SQLModel, table=True):
    """
    Основная сущность HelpDesk системы — заявка в поддержку.
    Связывает воедино клиента, исполнителя, категорию проблемы и историю её решения.
    Временные метки используются для расчета нарушений SLA.
    """
    id: int | None = Field(default=None, primary_key=True, index=True)
    header: str = Field(default=None, index=True, max_length=255, nullable=False)
    description: str = Field(default=None, nullable=False)
    
    # Важно для PostgreSQL: параметр name="..." внутри Enum() обязателен.
    # В Postgres Enum — это не просто ограничение строки, а отдельный кастомный тип данных 
    # (как INTEGER или VARCHAR). Если не дать ему имя, инструмент миграций (Alembic) 
    # не сможет его создать и будет выдавать ошибки при генерации миграций.
    status: Status = Field(sa_column=Column(Enum(Status, name="ticket_status_enum", values_callable=lambda x: [e.value for e in x]),
                                            nullable=False, server_default=Status.NEW.value))
    
    priority: Priority = Field(sa_column=Column(Enum(Priority, name="ticket_priority_enum",
                                                    values_callable=lambda x: [e.value for e in x]), nullable=False))
    
    response_deadline: datetime | None = Field(default=None)
    resolution_deadline: datetime | None = Field(default=None)
    
    # Временные метки для аналитики и SLA
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime | None = Field(default=None)
    closed_at: datetime | None = Field(default=None)
    
    # Внешние ключи
    creator_id: int = Field(foreign_key="user.id", nullable=False, index=True)
    assignee_id: int | None = Field(foreign_key="user.id", default=None, index=True)
    category_id: int = Field(foreign_key="category.id", nullable=False, index=True)
    
    category: Category = Relationship(back_populates="tickets_with_exact_category")
    creator: User = Relationship(back_populates="created_tickets", sa_relationship_kwargs={"foreign_keys": "Ticket.creator_id"})
    assignee: User | None = Relationship(back_populates="assigned_tickets", sa_relationship_kwargs={"foreign_keys": "Ticket.assignee_id"})
    comments: List[Comment] = Relationship(back_populates="ticket")
    attachments: List[Attachment] = Relationship(back_populates="ticket_with_attachment")
    histories_ticket: List[TicketHistory] = Relationship(back_populates="ticket_history")
    