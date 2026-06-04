from ..repositories.ticket_repo import TicketRepository
from ..schemas.ticket import TicketCreate, TicketUpdate
from ..models.ticket import Ticket

from typing import Sequence


class TicketService:
    def __init__(self, ticket_repo: TicketRepository):
        self.ticket_repo = ticket_repo
    
    
    async def create_ticket(self, ticket_in: TicketCreate, creator_id: int) -> Ticket:
        return await self.ticket_repo.create(ticket_in=ticket_in, creator_id=creator_id)

    
    async def get_ticket_by_id(self, id: int) -> Ticket:
        res = await self.ticket_repo.get_by_id(id)
        if res:
            return res
        else:
            raise ValueError("Такого тикета не существует")
    
    
    async def search_ticket_by_header(self, header: str) -> Sequence[Ticket]:
        res = await self.ticket_repo.search_by_header(header)
        return res if res else []
    
    
    async def update_ticket(self, ticket_id: int, update_in: TicketUpdate) -> Ticket:
        db_ticket = await self.get_ticket_by_id(ticket_id)
        update_data = update_in.model_dump(exclude_unset=True)
        return await self.ticket_repo.update(db_ticket, update_data)