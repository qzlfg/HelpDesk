from typing import Sequence, List

from ..repositories.ticket_repo import TicketRepository
from ..schemas.ticket import TicketCreate, TicketUpdate
from ..models.ticket import Ticket
from app.models.user import User
from app.models.enums import Status, Role


class TicketService:
    def __init__(self, ticket_repo: TicketRepository):
        self.ticket_repo = ticket_repo
    
    
    async def create_ticket(self, ticket_in: TicketCreate, creator_id: int) -> Ticket:
        return await self.ticket_repo.create(ticket_in=ticket_in, creator_id=creator_id)
    
    
    async def get_all_tickets(self,
                            user: User,
                            target_creator_id: int | None,
                            target_agent_id: int | None,
                            status: List[Status] | None,
                            category_id: List[int] | None,
                            skip: int, limit: int
    ) -> Sequence[Ticket]:
        if user.role == Role.CLIENT:
            return await self.ticket_repo.get_client_tickets(
                user.id,
                status,
                category_id,
                skip,
                limit
            )
        elif user.role == Role.AGENT:
            return await self.ticket_repo.get_client_tickets(
                user.id,
                status,
                category_id,
                skip,
                limit
            )
        else:
            return await self.ticket_repo.get_admin_tickets(
                target_creator_id,
                target_agent_id,
                status,
                category_id,
                skip,
                limit
            )

    
    async def get_ticket_by_id(self, id: int, user: User) -> Ticket | None:
        '''Возвращает тикет, если такой существует и если тикет принадлежит клиенту, иначе ошибка'''
        ticket = await self.ticket_repo.get_ticket_by_id(id)
    
        if not ticket:
            raise ValueError("Такого тикета не существует")
            
        if user.role == Role.CLIENT:
            if ticket.creator_id != user.id:
                raise ValueError("Это не ваш тикет")
                
        elif user.role == Role.AGENT:
            if ticket.assignee_id != user.id and ticket.status != Status.NEW:
                raise ValueError("Этот тикет не назначен вам")
                
        return ticket

            

    
    async def search_ticket_by_header(self, header: str) -> Sequence[Ticket]:
        '''Возвращает список тикетов по заголовку, если они есть, иначе пустой список'''
        res = await self.ticket_repo.search_by_header(header)
        return res if res else []
    
    
    async def update_ticket(self, ticket_id: int, update_in: TicketUpdate) -> Ticket:
        db_ticket = await self.ticket_repo.get_ticket_by_id(ticket_id)
        if not db_ticket:
            raise ValueError("Такого тикета не существует")
        update_data = update_in.model_dump(exclude_unset=True)
        return await self.ticket_repo.update(db_ticket, update_data)