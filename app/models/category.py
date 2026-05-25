from __future__ import annotations
from typing import TYPE_CHECKING, List
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from .ticket import Ticket
    from .sla_rule import SLARule
    

class Category(SQLModel, table=True):
    """
    Категория обращения (например, 'Техническая ошибка', 'Вопрос по оплате').
    Нужна для группировки заявок и маршрутизации. 
    В будущем к комбинации (Категория + Приоритет) будут привязываться правила SLA.
    """
    id: int | None = Field(default=None, primary_key=True, index=True)
    header: str = Field(nullable=False)
    description: str | None = Field(default=None)
    
    # Флаг мягкого удаления. Если False — клиенты больше не видят её при создании тикета,
    # но старые тикеты с этой категорией не ломаются.
    is_active: bool = Field(default=True)
    
    # Все тикеты, относящиеся к данной категории
    tickets_with_exact_category: list[Ticket] = Relationship(back_populates="category")
    
    sla_rules: List[SLARule] = Relationship(back_populates="category_sla")