from fastapi import APIRouter, Depends

from app.core.dependencies import get_comment_service, get_current_user

from app.models.user import User

from app.services.comment_service import CommentService

from app.schemas.comment import CommentResponse, CommentCreate, CommentUpdate

router = APIRouter()


@router.get("/tickets/{id}/comments", response_model=list[CommentResponse])
async def get_ticket_comments(
    id: int,
    user: User = Depends(get_current_user),
    comment_service: CommentService = Depends(get_comment_service)
):
    return await comment_service.get_comments_by_ticket_id(id, user)

@router.post("/tickets/{id}/comments", response_model=CommentResponse)
async def create_ticket_comment(
    id: int,
    data: CommentCreate,
    user: User = Depends(get_current_user),
    comment_service: CommentService = Depends(get_comment_service)
):
    return await comment_service.create_comment(id, data, user)

@router.patch("/comments/{id}", response_model=CommentResponse)
async def update_ticket_comment(
    id: int,
    update_data: CommentUpdate,
    user: User = Depends(get_current_user),
    comment_service: CommentService = Depends(get_comment_service)
):
    return await comment_service.update_comment(id, user, update_data)