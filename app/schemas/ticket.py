from pydantic import BaseModel, ConfigDict
from ..models.enums import Priority, Status
from datetime import datetime


class TicketBase(BaseModel):
    header: str
    description: str
    priority: Priority
    category_id: int


class TicketCreate(TicketBase):
    pass


class TicketResponse(TicketBase):
    id: int
    status: Status
    created_at: datetime
    updated_at: datetime | None = None
    closed_at: datetime | None = None
    creator_id: int
    assignee_id: int | None = None
    
    model_config = ConfigDict(from_attributes=True)
    

class TicketAdminResponse(TicketResponse):
    """
    Расширенная схема для админов и агентов.
    Включает метрики SLA и может включать историю/комментарии.
    """
    # Метрики SLA
    response_deadline: datetime | None = None
    resolution_deadline: datetime | None = None


class TicketUpdate(BaseModel):
    status: Status | None = None
    description: str | None = None
    priority: Priority | None = None
    assignee_id: int | None = None