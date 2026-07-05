from __future__ import annotations
from typing import TYPE_CHECKING

from datetime import datetime, timezone
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from .ticket import Ticket
    from .user import User


class TicketHistory(SQLModel, table=True):
    """
    Таблица для хранения истории изменений тикетов.
    Позволяет детально отследить, кто, когда и что изменил.
    """
    id: int | None = Field(default=None, primary_key=True, index=True)
    
    # Связь с тикетом. Если тикет удалят, история сотрется автоматически (CASCADE)
    ticket_id: int = Field(foreign_key="ticket.id", ondelete="CASCADE")
    
    # Кто изменил (ID пользователя из токена)
    changed_by_id: int = Field(foreign_key="user.id")
    
    # Какое поле изменилось (например: "status_id", "priority", "assignee_id")
    field_name: str = Field(nullable=False)
    
    # Старое и новое значение
    old_value: str | None = Field(default=None)
    new_value: str | None = Field(default=None)
    
    # Время изменения
    changed_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    ticket_history: Ticket = Relationship(back_populates="histories_ticket")
    user_changed: User = Relationship(back_populates="changed_tickets")