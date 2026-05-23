from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, Enum
from enum import IntEnum, Enum as PyEnum
from datetime import datetime

from user import User


class Priority(IntEnum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    URGENT = 4

    def __str__(self):
        return self.name.lower()

class Status(PyEnum, str):
    NEW = "new"
    ASSIGNED = "assigned"
    IN_PROGRESS = "in_progress"
    WAITING_FOR_CUSTOMER = "waiting_for_customer"
    RESOLVED = "resolved"
    CLOSED = "closed"
    

class Ticket(SQLModel, table=True):
    header: str | None = Field(default=None, index=True, max_length=255, nullable=False)
    description: str | None = Field(default=None, nullable=False)
    status: Status = Field(sa_column=Column(Enum(Status), nullable=False, server_default=Status.NEW.value))
    priority: Priority = Field(sa_column=Column(Enum(Priority), nullable=False))
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime | None = Field(default_factory=None)
    closed_at: datetime | None = Field(default_factory=None)
    creator: User = Field(foreign_key="user.id")
    
    
    creator_of_ticket: User = Relationship(back_populates="user")
    
    ... #Нужен agent и категория