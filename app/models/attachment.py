from __future__ import annotations
from typing import TYPE_CHECKING

from sqlmodel import SQLModel, Field, Relationship
from uuid import UUID, uuid4
from datetime import datetime, timezone

if TYPE_CHECKING:
    from .user import User
    from .ticket import Ticket
    from .comment import Comment

    
class Attachment(SQLModel, table=True):
    """
    Модель вложения (файла).
    Сами физические файлы хранятся на диске (или в S3 хранилище), 
    а в базе мы сохраняем только метаданные, чтобы знать, где искать файл, 
    как он назывался изначально и кому принадлежит.
    """
    id: int | None = Field(default=None, primary_key=True, index=True)
    file_path: str = Field(nullable=False)
    original_file_name: str = Field(nullable=False)
    
    # Уникальное имя файла на нашем сервере (чтобы два файла "1.jpg" не перезаписали друг друга).
    # Используем UUID4 для гарантии уникальности.
    file_name: UUID = Field(default_factory=uuid4, nullable=False)
    
    # MIME-тип файла (например, "image/png" или "application/pdf").
    # Нужен фронтенду, чтобы понимать, показывать это как картинку или отдавать как файл для скачивания.
    content_type: str = Field(nullable=False)
    
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    uploader_id: int = Field(foreign_key="user.id")
    ticket_id: int = Field(foreign_key="ticket.id")
    comment_id: int | None = Field(default=None, foreign_key="comment.id", nullable=True)
    
    ticket_with_attachment: Ticket = Relationship(back_populates="attachments")
    user: User = Relationship(back_populates="created_attachments")
    comment: Comment | None = Relationship(back_populates="attachments_with_comment")