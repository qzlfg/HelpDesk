from typing import Sequence

from ..models.comment import Comment
from ..schemas.comment import CommentUpdate, CommentCreate
from ..repositories.comment_repo import CommentRepository


class CommentService:
    def __init__(self, comment_repo: CommentRepository):
        self.comment_repo = comment_repo
    
    async def get_comment_by_id(self, id: int) -> Comment:
        res = await self.comment_repo.get_by_id(id)
        if not res:
            raise ValueError("Такого комментария не существует")
        return res

    async def get_comment_by_ticket_id(self, ticket_id: int) -> Sequence[Comment]:
        return await self.comment_repo.get_by_ticket_id(ticket_id)
    
    
    async def create_comment(self, comment_in: CommentCreate, creator_id: int) -> Comment:
        return await self.comment_repo.create(comment_in, creator_id)

    async def update_comment(self, comment_id: int, comment_in: CommentUpdate) -> Comment:
        comment_db = await self.get_comment_by_id(comment_id)
        update_data = comment_in.model_dump(exclude_unset=True)
        return await self.comment_repo.update(comment_db, update_data)