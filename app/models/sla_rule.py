from __future__ import annotations
from typing import TYPE_CHECKING

from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, Enum, UniqueConstraint
from .enums import Priority


if TYPE_CHECKING:
    from .category import Category


class SLARule(SQLModel, table=True):
    """
    Модель SLA-правила (Service Level Agreement).
    Работает как справочник-матрица для расчета дедлайнов новых тикетов.
    Когда клиент создает тикет, система ищет здесь правило по связке (Категория + Приоритет)
    и высчитывает точное время, до которого агент обязан ответить и решить проблему.
    """
    # Добавляем ограничение: в базе не может быть двух правил для одинаковой пары "Категория + Приоритет"
    __table_args__ = (
        UniqueConstraint("category_id", "priority", name="uq_category_priority_sla"),
    )
    
    id: int | None = Field(default=None, primary_key=True, index=True)
    
    # Название правила
    name: str = Field(nullable=False)
    
    priority: Priority = Field(sa_column=Column(Enum(Priority, name="ticket_priority_enum"), nullable=False))
    
    # Сколько минут дается агенту на первый ответ (перевод из статуса NEW).
    response_time_minutes: int = Field(default=12, nullable=False)
    
    # Сколько минут дается на окончательное закрытие тикета (перевод в RESOLVED).
    resolution_time_minutes: int = Field(nullable=False)
    
    # Флаг активности. Если False, правило временно отключено админом, 
    # и система будет использовать дефолтные значения.
    is_active: bool = Field(default=True, nullable=False)
    
    category_id: int = Field(foreign_key="category.id", index=True)
    
    category_sla: Category = Relationship(back_populates="sla_rules")