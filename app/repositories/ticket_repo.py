from sqlmodel import select, col
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Sequence


from ..models.ticket import Ticket
from ..schemas.ticket import TicketCreate


class TicketRepository:
    """
    Слой доступа к данным для сущности Ticket.
    Изолирует написание SQL-запросов от остальной бизнес-логики приложения.
    """
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, ticket_id: int) -> Ticket | None:
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
        
        self.session.add(ticket_data)
        await self.session.flush() 
        await self.session.refresh(ticket_data)
        
        return db_ticket

    async def update(self, db_ticket: Ticket, update_data: dict) -> Ticket:
        """
        Обновляет существующий тикет.
        Принимает объект из БД и словарь с новыми данными.
        """
        for key, value in update_data.items():
            setattr(db_ticket, key, value)
            
        self.session.add(db_ticket)
        await self.session.flush()
        await self.session.refresh(db_ticket)
        
        return db_ticket