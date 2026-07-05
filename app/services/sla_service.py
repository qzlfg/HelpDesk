from typing import Sequence

from ..repositories.sla_repo import SLARuleRepository
from ..schemas.sla_rule import CreateSLARule, SLARuleUpdate
from ..models.sla_rule import SLARule


class SLARuleService:
    def __init__(self, sla_repo: SLARuleRepository) -> None:
        self.sla_repo = sla_repo
    
    async def create(self, rule_in: CreateSLARule) -> SLARule:
        sla_rule = await self.sla_repo.find_matching_rule(priority=rule_in.priority, category_id=rule_in.category_id)
        
        if sla_rule:
            return sla_rule

        return await self.sla_repo.create(rule_in=rule_in)

    async def get_by_id(self, rule_id: int) -> SLARule:
        sla_rule = await self.sla_repo.get_by_id(rule_id=rule_id)
        
        if sla_rule:
            return sla_rule
        
        raise ValueError("Такого SLARule не существует")
    
    async def get_all_active(self) -> Sequence[SLARule]:
        return await self.sla_repo.get_all_active()
    
    async def update(self, sla_id: int, sla_update: SLARuleUpdate) -> SLARule:
        sla_rule = await self.get_by_id(sla_id)
        update_data = sla_update.model_dump(exclude_unset=True)
        return await self.sla_repo.update(sla_rule, update_data)