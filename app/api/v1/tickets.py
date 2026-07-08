from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List

from app.services.ticket_service import TicketService

from app.models.user import User
from app.models.ticket import Ticket
from app.models.ticket_history import TicketHistory
from app.models.enums import Status, Role

from app.schemas.ticket import TicketCreate, TicketResponse, TicketAdminResponse
from app.schemas.ticket_history import TicketHistoryCreate

from app.core.dependencies import get_current_user, get_ticket_service


router = APIRouter()


@router.post("/tickets", response_model=TicketResponse)
async def create_ticket(
    ticket_in: TicketCreate,
    cur_user: User = Depends(get_current_user),
    ticket_service: TicketService = Depends(get_ticket_service)
):
    assert cur_user.id is not None, "У пользователя из БД всегда есть ID"
    
    return await ticket_service.create_ticket(ticket_in=ticket_in, creator_id=cur_user.id)


@router.get("/tickets", response_model=list[TicketResponse | TicketAdminResponse])
async def get_all_tickets(
    skip: int = 0,
    limit: int = 15,
    target_creator_id: int | None = Query(default=None, description="Фильтр по автору (только для админов)"),
    target_agent_id: int | None = Query(default=None, description="Фильтр по агенту (только для админов)"),
    statuses: List[Status] | None = Query(None),
    category_ids: List[int] | None = Query(None),
    cur_user: User = Depends(get_current_user),
    ticket_service: TicketService = Depends(get_ticket_service)
):
    assert cur_user.id is not None, "У пользователя из БД всегда есть ID"
    
    return await ticket_service.get_all_tickets(
        cur_user,
        target_creator_id,
        target_agent_id,
        statuses,
        category_ids,
        skip,
        limit
    )


@router.get("/tickets/{id}", response_model=TicketResponse | TicketAdminResponse)
async def get_one_ticket(
    id: int, #id тикета
    cur_user: User = Depends(get_current_user),
    ticket_service: TicketService = Depends(get_ticket_service)
):
    
    assert cur_user.id is not None, "У пользователя из БД всегда есть ID"
    
    return await ticket_service.get_ticket_by_id(id, cur_user)