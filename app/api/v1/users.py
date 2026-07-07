from fastapi import APIRouter, Depends, HTTPException, status


from app.core.dependencies import get_user_service, get_current_admin, get_current_user

from app.schemas.user import UserCreate, UserResponse, UserUpdateAdmin

from app.services.user_service import UserService

from app.models.user import User


router = APIRouter()

@router.post("/register", response_model=UserResponse)
async def registry(
    user_in: UserCreate,
    user_service: UserService = Depends(get_user_service)
):
    try:
        new_user = await user_service.create_user(user_in)
        
        return new_user
    
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/users")
async def get_all_users(
    skip: int = 0,
    limit: int = 100,
    admin: User = Depends(get_current_admin),
    user_service: UserService = Depends(get_user_service)
):
    return await user_service.get_all_users(skip, limit)


@router.get("/users/me")
async def get_user_profile(
    cur_user: User = Depends(get_current_user),
):
    return cur_user

@router.patch("/users/{id}")
async def change_user_data(
    id: int,
    update_in: UserUpdateAdmin,
    user_service: UserService = Depends(get_user_service),
    admin: User = Depends(get_current_admin),
):
    return await user_service.update_user_by_admin(id, update_in)