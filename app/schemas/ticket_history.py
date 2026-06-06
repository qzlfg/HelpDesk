from pydantic import BaseModel

class TicketHistoryCreate(BaseModel):
    ticket_id: int
    field_name: str
    old_value: str
    new_value: str