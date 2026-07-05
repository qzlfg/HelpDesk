from pydantic import BaseModel, EmailStr, ConfigDict
from ..models.enums import Role


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserResponse(UserBase):
    id: int
    role: Role
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


class UserUpdate(BaseModel):
    email: EmailStr | None = None
    password: str | None = None


class UserUpdateAdmin(BaseModel):
    email: EmailStr | None = None
    password: str | None = None
    role: str | None = None