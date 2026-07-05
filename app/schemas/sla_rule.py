from pydantic import BaseModel, ConfigDict
from ..models.enums import Priority


class BaseSLARule(BaseModel):
    """
    Базовая схема SLA-правила.
    Включает все основные параметры, которые описывают суть дедлайнов.
    """
    name: str
    priority: Priority
    response_time_minutes: int
    resolution_time_minutes: int
    category_id: int

class CreateSLARule(BaseSLARule):
    pass

class ResponseSLARule(BaseSLARule):
    id: int
    is_active: bool
    
    model_config = ConfigDict(from_attributes=True)
    

class SLARuleUpdate(BaseModel):
    """
    Схема для редактирования правила.
    Все поля опциональны, чтобы можно было, например, просто выключить 
    правило (is_active=False), не пересылая заново его название и приоритет.
    """
    name: str | None = None
    priority: Priority | None = None
    response_time_minutes: int | None = None
    resolution_time_minutes: int | None = None
    category_id: int | None = None
    is_active: bool | None = None