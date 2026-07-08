from sqlmodel import select, col, and_
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Sequence, List
from datetime import datetime, timezone


from ..models.ticket import Ticket
from ..schemas.ticket import TicketCreate
from app.models.enums import Status


class TicketRepository:
    """
    Слой доступа к данным для сущности Ticket.
    """
    def __init__(self, session: AsyncSession):
        self.session = session
        
        
    async def get_client_tickets(self,
                                creator_id: int,
                                ticket_statuses: List[Status] | None,
                                category_ids: List[int] | None,
                                skip: int, limit: int,
    ) -> Sequence[Ticket]:
        query = select(Ticket).where(Ticket.creator_id == creator_id)
        
        if ticket_statuses:
            query = query.where(col(Ticket.status).in_(ticket_statuses))
        else:
            query = query.where(Ticket.status != Status.CLOSED)
            
        if category_ids:
            query = query.where(col(Ticket.category_id).in_(category_ids))
            
        query = query.order_by(col(Ticket.created_at)).offset(skip).limit(limit)
        
        result = await self.session.execute(query)
        return result.scalars().all()
    
    
    async def get_agent_tickets(self,
                                agent_id: int,
                                ticket_statuses: List[Status] | None,
                                category_ids: List[int] | None,
                                skip: int, limit: int,
    ) -> Sequence[Ticket]:
        query = select(Ticket).where(Ticket.assignee_id == agent_id)
        
        if ticket_statuses:
            query = query.where(col(Ticket.status).in_(ticket_statuses))
        else:
            query = query.where(Ticket.status != Status.CLOSED)
            
        if category_ids:
            query = query.where(col(Ticket.category_id).in_(category_ids))
            
        query = query.order_by(col(Ticket.created_at)).offset(skip).limit(limit)
        
        result = await self.session.execute(query)
        return result.scalars().all()
    
    
    async def get_admin_tickets(self,
        creator_id: int | None,
        agent_id: int | None,
        ticket_statuses: List[Status] | None,
        category_ids: List[int] | None,
        skip: int, limit: int,
    ) -> Sequence[Ticket]:
        query = select(Ticket)
        
        if creator_id:
            query = query.where(Ticket.creator_id == creator_id)
            
        if agent_id:
            query = query.where(Ticket.assignee_id == agent_id)
        
        if ticket_statuses:
            query = query.where(col(Ticket.status).in_(ticket_statuses))
        else:
            query = query.where(Ticket.status != Status.CLOSED)
            
        if category_ids:
            query = query.where(col(Ticket.category_id).in_(category_ids))
            
        query = query.order_by(col(Ticket.created_at)).offset(skip).limit(limit)
        
        result = await self.session.execute(query)
        return result.scalars().all()


    async def get_ticket_by_id(self, ticket_id: int) -> Ticket | None:
        """
        Ищет тикет по ID.
        Возвращает объект Ticket или None, если такого тикета нет.
        """
        statement = select(Ticket).where(Ticket.id == ticket_id)
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()

    async def search_by_header(self, search_query: str) -> Sequence[Ticket]:
        """
        Ищет тикет по заголовку.
        """
        statement = select(Ticket).where(col(Ticket.header).ilike(f"%{search_query}%"))
        result = await self.session.execute(statement)
        return result.scalars().all()

    async def create(self, ticket_in: TicketCreate, creator_id: int) -> Ticket:
        """
        Создает нового пользователя в базе данных.
        """
        ticket_data = ticket_in.model_dump()
        ticket_data["creator_id"] = creator_id
        
        db_ticket = Ticket(**ticket_data)
        
        self.session.add(db_ticket)
        await self.session.flush() 
        await self.session.refresh(db_ticket)
        
        return db_ticket
    

    async def update(self, db_ticket: Ticket, update_data: dict) -> Ticket:
        """
        Обновляет существующий тикет.
        Принимает объект из БД и словарь с новыми данными.
        """
        update_data["updated_at"] = datetime.now(timezone.utc)
        for key, value in update_data.items():
            setattr(db_ticket, key, value)
            
        self.session.add(db_ticket)
        await self.session.flush()
        await self.session.refresh(db_ticket)
        
        return db_ticket