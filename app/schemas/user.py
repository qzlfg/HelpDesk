from pydantic import BaseModel, EmailStr, ConfigDict
from ..models.enums import Role


class UserBase(BaseModel):
    email: EmailStr
    role: Role
    
class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int

    model_config = ConfigDict(from_attributes=True)