from fastapi import APIRouter, Depends, HTTPException, status


from app.core.dependencies import get_user_service

from app.schemas.user import UserCreate, UserResponse

from app.services.user_service import UserService


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