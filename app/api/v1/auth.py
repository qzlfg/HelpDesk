from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from ...core.dependencies import get_auth_service
from ...services.auth_service import AuthService


router = APIRouter()

@router.post("/login")
async def authenticate(form_data: OAuth2PasswordRequestForm = Depends(),
    auth_service: AuthService = Depends(get_auth_service)) -> dict:
    token = await auth_service.authenticate_user(email=form_data.username, password=form_data.password)
    return {"access_token": token, "token_type": "bearer"}