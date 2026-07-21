from pydantic import BaseModel, ConfigDict
from datetime import datetime

class TicketHistoryCreate(BaseModel):
    ticket_id: int
    field_name: str
    old_value: str
    new_value: str

class TicketHistoryResponse(BaseModel):
    id: int
    field_name: str
    old_value: str | None
    new_value: str | None
    changed_by_id: int
    changed_at: datetime
    
    model_config = ConfigDict(from_attributes=True)