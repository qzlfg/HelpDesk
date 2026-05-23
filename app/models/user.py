from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, Enum
from enum import Enum as PyEnum

from ticket import Ticket


class Role(str, PyEnum):
    CLIENT = "client"
    AGENT = "agent"
    ADMIN = "admin"


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True, index=True)
    email: str = Field(unique=True, index=True, max_length=255)
    password_hash: str = Field(max_length=255)
    role: Role = Field(sa_column=Column(Enum(Role), nullable=False, server_default=Role.CLIENT.value))
    
    created_tickets: list[Ticket] = Relationship(back_populates="ticket")