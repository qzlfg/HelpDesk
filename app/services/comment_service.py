from typing import Sequence
from datetime import datetime, timezone

from ..models.comment import Comment
from ..schemas.comment import CommentUpdate, CommentCreate
from ..repositories.comment_repo import CommentRepository
from ..repositories.ticket_repo import TicketRepository
from ..models.user import User
from ..models.enums import Role


class CommentService:
    def __init__(self, comment_repo: CommentRepository, ticket_repo: TicketRepository):
        self.comment_repo = comment_repo
        self.ticket_repo = ticket_repo
    
    async def get_comment_by_ticket_id(self, id: int) -> Comment:
        res = await self.comment_repo.get_by_id(id)
        if not res:
            raise ValueError("Такого комментария не существует")
        return res


    async def get_comments_by_ticket_id(self, ticket_id: int, user: User) -> Sequence[Comment]:
        """
        Просмотр всех комментариев тикета
        """
        ticket = await self.ticket_repo.get_ticket_by_id(ticket_id)
        
        if not ticket:
            raise ValueError("Такого тикета не существует")
        
        if user.role == Role.CLIENT:
            if ticket.creator_id != user.id:
                raise ValueError("Этот тикет вам не принадлежит")
        elif user.role == Role.AGENT:
            if ticket.assignee_id is not None and ticket.assignee_id != user.id:
                raise ValueError("Этот тикет вам не принадлежит")
            
        only_public = (user.role == Role.CLIENT)
        
        return await self.comment_repo.get_by_ticket_id(ticket_id, only_public)
    
    
    async def create_comment(self, ticket_id: int, comment_in: CommentCreate, user: User) -> Comment:
        
        ticket = await self.ticket_repo.get_ticket_by_id(ticket_id)
        
        if not ticket:
            raise ValueError("Такого тикета не существует")
        
        if user.role == Role.CLIENT:
            if ticket.creator_id != user.id:
                raise ValueError("Этот тикет вам не принадлежит")
            comment_in.is_internal = False
            
        elif user.role == Role.AGENT:
            if ticket.assignee_id is not None and ticket.assignee_id != user.id:
                raise ValueError("Этот тикет вам не принадлежит")
            
        assert user.id is not None, "Пользователь обязан иметь ID"
        
        return await self.comment_repo.create(ticket_id, comment_in, user.id)


    async def update_comment(self, comment_id: int, user: User, comment_in: CommentUpdate) -> Comment:
        
        comment = await self.comment_repo.get_by_id(comment_id)
        if not comment:
            raise ValueError("Такого комментария не существует")
        
        ticket = await self.ticket_repo.get_ticket_by_id(comment.ticket_id)
        if not ticket:
            raise ValueError("Такого тикета не существует")
        
        
        if user.role in (Role.CLIENT, Role.AGENT):
            if comment.creator_id != user.id:
                raise ValueError("Вы не можете редактировать чужие сообщения")
            
        if user.role == Role.CLIENT:    
            if ticket.creator_id != user.id:
                raise ValueError("Этот тикет вам не принадлежит")
            
        elif user.role == Role.AGENT:
            if ticket.assignee_id is not None and ticket.assignee_id != user.id:
                raise ValueError("Этот тикет вам не принадлежит")
        
            
        assert user.id is not None, "Пользователь обязан иметь ID"
        
        updated_data = {
            "content": comment_in.content,
            "updated_at": datetime.now(timezone.utc)
        }
        
        return await self.comment_repo.update(comment, updated_data)