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
    
class UserUpdate(BaseModel):
    email: EmailStr | None = None
    password: str | None = None
    #Админ может поменять роль (с юзера на агента)
    role: Role | None = None