from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Sequence

from ..models.sla_rule import SLARule
from ..models.enums import Priority
from ..schemas.sla_rule import CreateSLARule


class SLARuleRepository:
    """
    Слой доступа к данным для сущности SLARule.
    Отвечает за хранение настроек времени реакции и решения заявок.
    """
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, rule_id: int) -> SLARule | None:
        """
        Ищет SLA-правило по ID.
        """
        statement = select(SLARule).where(SLARule.id == rule_id)
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()

    async def get_all_active(self) -> Sequence[SLARule]:
        """
        Возвращает список всех активных SLA-правил.
        Полезно для панели администратора.
        """
        statement = select(SLARule).where(SLARule.is_active)
        result = await self.session.execute(statement)
        return result.scalars().all()

    async def find_matching_rule(self, priority: Priority, category_id: int) -> SLARule | None:
        """
        Ищет активное правило, которое совпадает по приоритету и категории.
        Вызывается АВТОМАТИЧЕСКИ при создании каждого нового тикета.
        """
        statement = (
            select(SLARule)
            .where(
                SLARule.is_active,
                SLARule.priority == priority,
                SLARule.category_id == category_id
            )
        )
        result = await self.session.execute(statement)

        return result.scalar_one_or_none()

    async def create(self, rule_in: CreateSLARule) -> SLARule:
        """
        Создает новое SLA-правило.
        """
        db_rule = SLARule(**rule_in.model_dump())
        
        self.session.add(db_rule)
        await self.session.flush()
        await self.session.refresh(db_rule)
        
        return db_rule

    async def update(self, db_rule: SLARule, update_data: dict) -> SLARule:
        """
        Обновляет существующее SLA-правило (например, меняет тайминги).
        """
        for key, value in update_data.items():
            setattr(db_rule, key, value)
            
        self.session.add(db_rule)
        await self.session.flush()
        await self.session.refresh(db_rule)
        
        return db_rule