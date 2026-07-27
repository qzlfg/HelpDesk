from typing import Annotated
from fastapi import APIRouter, Depends

from app.core.dependencies import get_category_service, get_current_admin, get_current_user
from app.models.user import User
from app.services.category_service import CategoryService
from app.schemas.category import CategoryCreate, CategoryResponse, CategoryUpdate


router = APIRouter()

@router.get("/categories", response_model=list[CategoryResponse])
async def get_categories(
    user: Annotated[User, Depends(get_current_user)],
    category_service: Annotated[CategoryService, Depends(get_category_service)],
):
    return await category_service.get_active_categories()

@router.post("/categories", response_model=CategoryResponse)
async def create_category(
    category_in: CategoryCreate,
    user: Annotated[User, Depends(get_current_admin)],
    category_service: Annotated[CategoryService, Depends(get_category_service)],
):
    return await category_service.create_category(category_in)

@router.patch("/categories/{category_id}")
async def update_category(
    category_id: int,
    update_data: CategoryUpdate,
    user: Annotated[User, Depends(get_current_admin)],
    category_service: Annotated[CategoryService, Depends(get_category_service)],
):
    return await category_service.update_category(category_id, update_data)