from __future__ import annotations
from typing import TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, Enum
from enum import Enum as PyEnum
from datetime import datetime


if TYPE_CHECKING:
    from app.models.user import User
    from app.models.category import Category

class Priority(str, PyEnum):
    """
    Уровень критичности тикета. 
    Влияет на то, как быстро агент должен отреагировать и решить проблему (SLA).
    """
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"

    def __str__(self):
        return self.name.lower()

class Status(PyEnum, str):
    """
    Жизненный цикл тикета. Позволяет отслеживать текущее состояние проблемы:
    - NEW: только создан, никто не взял в работу.
    - ASSIGNED: назначен агент, но работа еще не начата.
    - IN_PROGRESS: агент активно решает проблему.
    - WAITING_FOR_CUSTOMER: агент задал вопрос клиенту и ждет ответа (таймер SLA на решение обычно ставится на паузу).
    - RESOLVED: агент пометил проблему как решенную (но клиент еще может переоткрыть).
    - CLOSED: окончательно закрыт, изменения запрещены.
    """
    NEW = "new"
    ASSIGNED = "assigned"
    IN_PROGRESS = "in_progress"
    WAITING_FOR_CUSTOMER = "waiting_for_customer"
    RESOLVED = "resolved"
    CLOSED = "closed"
    

class Ticket(SQLModel, table=True):
    """
    Основная сущность HelpDesk системы — заявка в поддержку.
    Связывает воедино клиента, исполнителя, категорию проблемы и историю её решения.
    Временные метки используются для расчета нарушений SLA.
    """
    id: int | None = Field(default=None, primary_key=True)
    header: str = Field(default=None, index=True, max_length=255, nullable=False)
    description: str = Field(default=None, nullable=False)
    
    # Важно для PostgreSQL: параметр name="..." внутри Enum() обязателен.
    # В Postgres Enum — это не просто ограничение строки, а отдельный кастомный тип данных 
    # (как INTEGER или VARCHAR). Если не дать ему имя, инструмент миграций (Alembic) 
    # не сможет его создать и будет выдавать ошибки при генерации миграций.
    status: Status = Field(sa_column=Column(Enum(Status, name="ticket_status_enum"), nullable=False, server_default=Status.NEW.value))
    
    priority: Priority = Field(sa_column=Column(Enum(Priority), nullable=False))
    
    # Временные метки для аналитики и SLA
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime | None = Field(default=None)
    closed_at: datetime | None = Field(default_factory=None)
    
    # Внешние ключи
    creator_id: int = Field(foreign_key="user.id", nullable=False)
    assignee_id: int | None = Field(foreign_key="user.id", default=None)
    category_id: int = Field(foreign_key="category.id", nullable=False)
    
    category: Category = Relationship(back_populates="tickets_with_exact_category")
    creator: User = Relationship(back_populates="created_tickets", sa_relationship_kwargs={"foreign_keys": "Ticket.creator_id"})
    assignee: User | None = Relationship(back_populates="assigned_tickets", sa_relationship_kwargs={"foreign_keys": "Ticket.assignee_id"})
    