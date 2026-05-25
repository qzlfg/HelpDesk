from pydantic import BaseModel, ConfigDict

class CategoryBase(BaseModel):
    header: str
    description: str | None = None
    
class CategoryCreate(CategoryBase):
    pass

class CategoryResponse(CategoryBase):
    id: int
    is_active: bool
    
    model_config = ConfigDict(from_attributes=True)
    
class CategoryUpdate(BaseModel):
    """
    Все поля опциональны. Админ может, например, передать только {"is_active": false},
    чтобы скрыть категорию, не меняя её текст.
    """
    header: str | None = None
    description: str | None = None
    is_active: bool | None = None