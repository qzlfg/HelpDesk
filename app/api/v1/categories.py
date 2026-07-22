from fastapi import APIRouter, Depends

from app.core.dependencies import get_category_service, get_current_admin, get_current_user
from app.models.user import User
from app.services.category_service import CategoryService
from app.schemas.category import CategoryCreate, CategoryResponse, CategoryUpdate


router = APIRouter()

@router.get("/categories", response_model=list[CategoryResponse])
async def get_categories(
    user: User = Depends(get_current_user),
    category_service: CategoryService = Depends(get_category_service)
):
    return await category_service.get_active_categories()

@router.post("/categories", response_model=CategoryResponse)
async def create_category(
    category_in: CategoryCreate,
    user: User = Depends(get_current_admin),
    category_service: CategoryService = Depends(get_category_service)
):
    return await category_service.create_category(category_in)

@router.patch("/categories/{id}")
async def update_category(
    id: int,
    update_data: CategoryUpdate,
    user: User = Depends(get_current_admin),
    category_service: CategoryService = Depends(get_category_service)
):
    return await category_service.update_category(id, update_data)