from pydantic import BaseModel, ConfigDict
from datetime import datetime


class CommentCreate(BaseModel):
    content: str
    ticket_id: int


class CommentResponse(BaseModel):
    id: int
    content: str | None = None
    created_at: datetime
    creator_id: int
    ticket_id: int
    
    is_internal: bool
    
    model_config = ConfigDict(from_attributes=True)


class CommentUpdate(BaseModel):
    content: str | None = None