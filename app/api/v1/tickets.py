from fastapi import APIRouter, Depends, Query, Body
from typing import List

from app.services.ticket_service import TicketService

from app.models.user import User
from app.models.ticket_history import TicketHistory
from app.models.enums import Status, Role

from app.schemas.ticket import TicketCreate, TicketResponse, TicketAdminResponse, TicketStatusUpdate, TicketDescriptionUpdate, TicketPriorityUpdate
from app.schemas.ticket_history import TicketHistoryCreate

from app.core.dependencies import get_current_user, get_ticket_service, get_current_agent, get_current_admin


router = APIRouter()


@router.post("/tickets", response_model=TicketResponse)
async def create_ticket(
    ticket_in: TicketCreate,
    cur_user: User = Depends(get_current_user),
    ticket_service: TicketService = Depends(get_ticket_service)
):
    assert cur_user.id is not None, "У пользователя из БД всегда есть ID"
    
    return await ticket_service.create_ticket(ticket_in=ticket_in, creator_id=cur_user.id)


@router.get("/tickets")
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
    
    raw_tickets = await ticket_service.get_all_tickets(
        cur_user,
        target_creator_id,
        target_agent_id,
        statuses,
        category_ids,
        skip,
        limit
    )
    
    if cur_user.role in (Role.CLIENT, Role.AGENT):
        return [TicketResponse.model_validate(t) for t in raw_tickets]

    return [TicketAdminResponse.model_validate(t) for t in raw_tickets]


@router.get("/tickets/{id}")
async def get_one_ticket(
    id: int, #id тикета
    cur_user: User = Depends(get_current_user),
    ticket_service: TicketService = Depends(get_ticket_service)
):
    
    assert cur_user.id is not None, "У пользователя из БД всегда есть ID"
    
    raw_ticket = await ticket_service.get_ticket_by_id(id, cur_user)
    
    if cur_user.role in (Role.CLIENT, Role.AGENT):
        return TicketResponse.model_validate(raw_ticket)
    return TicketAdminResponse.model_validate(raw_ticket)


@router.patch("/tickets/{id}/assign")
async def assign_ticket(
    id: int, #id тикета
    staff_user: User = Depends(get_current_agent),
    assign_id: int | None = Body(default=None, embed=False),
    ticket_service: TicketService = Depends(get_ticket_service)
):
    raw_ticket = ticket_service.assign_ticket(id, staff_user, assign_id)
    
    if staff_user.role == Role.AGENT:
        return TicketResponse.model_validate(raw_ticket)
    
    return TicketAdminResponse.model_validate(raw_ticket)


@router.patch("/tickets/{id}/status")
async def update_ticket_status(
    id: int,
    update_data: TicketStatusUpdate,
    staff_user: User = Depends(get_current_agent),
    ticket_service: TicketService = Depends(get_ticket_service)
):
    
    raw_ticket = ticket_service.update_ticket_status(id, staff_user, update_data.status)
    
    if staff_user.role == Role.AGENT:
        return TicketResponse.model_validate(raw_ticket)
    
    return TicketAdminResponse.model_validate(raw_ticket)


@router.patch("/tickets/{id}/description")
async def update_ticket_desription(
    id: int,
    update_data: TicketDescriptionUpdate,
    user: User = Depends(get_current_user),
    ticket_service: TicketService = Depends(get_ticket_service)
):
    raw_ticket = ticket_service.update_ticket_description(id, user, update_data.description)