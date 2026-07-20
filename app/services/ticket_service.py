from typing import Sequence, List, Any, Dict
from datetime import datetime, timezone

from ..repositories.ticket_repo import TicketRepository
from ..schemas.ticket import TicketCreate, TicketUpdate, TicketStatusUpdate
from ..models.ticket import Ticket
from ..schemas.ticket_history import TicketHistoryCreate
from ..repositories.ticket_history_repo import TicketHistoryRepository
from app.models.user import User
from app.models.enums import Status, Role


class TicketService:
    def __init__(self, ticket_repo: TicketRepository, ticket_hitory_repo: TicketHistoryRepository):
        self.ticket_repo = ticket_repo
        self.ticket_history_repo = ticket_hitory_repo
    
    
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
        assert user.id is not None, "Пользователь должен иметь ID"
        
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
    
    
    async def assign_ticket(self, ticket_id: int, staff_user: User, assign_id: int | None = None):
        ticket = await self.ticket_repo.get_ticket_by_id(ticket_id)
        
        if not ticket:
            raise ValueError("Такого тикета не существует")
        
        final_assignee_id = None
        
        if staff_user.role == Role.AGENT:
            final_assignee_id = staff_user.id
        
        else:
            if assign_id is None:
                raise ValueError("Администратор обязан указать ID агента для назначения")
            final_assignee_id = assign_id
            
        assert staff_user.id is not None, "У пользователя обязан быть ID"
        
        update_data = {
        "assignee_id": final_assignee_id,
        "status": Status.IN_PROGRESS
        }
        
        history_record = TicketHistoryCreate(
            ticket_id=ticket_id,
            field_name="status",
            old_value=str(ticket.assignee_id),
            new_value=str(final_assignee_id)
        )
        
        
        
        updated_ticket = await self.ticket_repo.update(ticket, update_data)
        
        await self.ticket_history_repo.create(history_record, staff_user.id)
        
        return updated_ticket
    
    async def update_ticket_status(self, ticket_id: int, user: User, new_status: TicketStatusUpdate):
        ticket = await self.ticket_repo.get_ticket_by_id(ticket_id)
        
        if not ticket:
            raise ValueError("Такого тикета не существует")
        
        cur_ticket_status = ticket.status #текущий статус тикета
        
        if cur_ticket_status == new_status.status:
            return ticket
        
        if user.role == Role.AGENT:
            if ticket.assignee_id != user.id:
                raise ValueError("Этот тикет не вам назначен")
            if cur_ticket_status == Status.CLOSED:
                raise ValueError("Этот тикет уже закрыт")
        
        
        assert user.id is not None, "У авторизованного пользователя обязан быть ID"
        
        
        update_data: Dict[str, Any] = {
            "status": new_status.status
        }
        
        if new_status.status == Status.CLOSED:
            update_data["closed_at"] = datetime.now(timezone.utc)
        elif cur_ticket_status == Status.CLOSED and new_status.status != Status.CLOSED:
            update_data["closed_at"] = None
            
        
        updated_ticket = await self.ticket_repo.update(ticket, update_data)
        
        history_record = TicketHistoryCreate(
            ticket_id=ticket_id,
            field_name="status",
            old_value=cur_ticket_status,
            new_value=str(new_status.status)
        )
        
        await self.ticket_history_repo.create(history_record, user.id)
        
        return updated_ticket