from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.core.dependencies import get_current_admin, get_current_user, get_user_service
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse, UserUpdateAdmin
from app.services.user_service import UserService

CurrentUser = Annotated[User, Depends(get_current_user)]
CurrentAdmin = Annotated[User, Depends(get_current_admin)]
UserSvc = Annotated[UserService, Depends(get_user_service)]


router = APIRouter()

@router.post("/register", response_model=UserResponse)
async def registry(
    user_in: UserCreate,
    user_service: UserSvc
):
    try:
        return await user_service.create_user(user_in)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/users", response_model=list[UserResponse])
async def get_all_users(
    admin: CurrentAdmin,
    user_service: UserSvc,
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 100
):
    return await user_service.get_all_users(skip, limit)


@router.get("/users/me", response_model=UserResponse)
async def get_user_profile(
    cur_user: CurrentUser,
):
    return cur_user


@router.patch("/users/{id}", response_model=UserResponse)
async def change_user_data(
    id: int,
    update_in: UserUpdateAdmin,
    admin: CurrentAdmin,
    user_service: UserSvc
):
    return await user_service.update_user_by_admin(id, update_in)