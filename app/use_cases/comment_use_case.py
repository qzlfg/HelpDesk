from ..schemas.comment import CommentCreate
from ..models.comment import Comment
from ..services.comment_service import CommentService
from ..services.ticket_service import TicketService

class CreateCommentUseCase:
    """
    Оркестратор для процесса создания нового комментария.
    Связывает независимые сервисы TicketService и CommentService вместе.
    """
    def __init__(self, comment_service: CommentService, ticket_service: TicketService):
        self.comment_service = comment_service
        self.ticket_service = ticket_service

    async def execute(self, comment_in: CommentCreate, creator_id: int) -> Comment:
        await self.ticket_service.get_ticket_by_id(comment_in.ticket_id)

        return await self.comment_service.create_comment(comment_in, creator_id)