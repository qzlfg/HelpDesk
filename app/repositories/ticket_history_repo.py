from sqlmodel import select, col
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Sequence


from ..models.ticket_history import TicketHistory
from ..schemas.ticket_history import TicketHistoryCreate


class TicketHistoryRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
        
    async def create(self, history_entry: TicketHistoryCreate, changed_by_id: int) -> TicketHistory:
        ticket_data = history_entry.model_dump()
        ticket_data["changed_by_id"] = changed_by_id
        
        ticket_db = TicketHistory(**ticket_data)
        
        self.session.add(ticket_db)
        await self.session.flush()
        await self.session.refresh(ticket_db)
        
        return ticket_db
        
    
    async def get_by_ticket_id(self, ticket_id: int) -> Sequence[TicketHistory]:
        statement = select(TicketHistory).where(TicketHistory.ticket_id == ticket_id).order_by(col(TicketHistory.changed_at))
        result = await self.session.execute(statement)
        return result.scalars().all()