from pydantic import BaseModel, ConfigDict
from datetime import datetime
from uuid import UUID


class AttachmentResponse(BaseModel):
    """
    Схема ответа API для вложения.
    Мы отдаем фронтенду всё необходимое, чтобы он мог отрисовать ссылку на файл
    и показать, когда и кем он был загружен.
    """
    id: int
    file_path: str
    original_file_name: str
    file_name: UUID
    content_type: str
    created_at: datetime
    
    uploader_id: int
    ticket_id: int
    comment_id: int | None = None
    
    model_config = ConfigDict(from_attributes=True)