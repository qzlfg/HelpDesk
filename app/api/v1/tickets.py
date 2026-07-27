from fastapi import APIRouter, Depends, Query, Body
from typing import Annotated, List

from app.services.ticket_service import TicketService

from app.models.user import User
from app.models.ticket_history import TicketHistory
from app.models.enums import Status, Role

from app.schemas.ticket import TicketCreate, TicketResponse, TicketAdminResponse, TicketStatusUpdate, TicketDescriptionUpdate, TicketPriorityUpdate
from app.schemas.ticket_history import TicketHistoryResponse

from app.core.dependencies import get_current_user, get_ticket_service, get_current_agent, get_current_admin


router = APIRouter()

CurrentUser = Annotated[User, Depends(get_current_user)]
CurrentAgent = Annotated[User, Depends(get_current_agent)]
TicketServiceDep = Annotated[TicketService, Depends(get_ticket_service)]


@router.post("/tickets", response_model=TicketResponse)
async def create_ticket(
    ticket_in: TicketCreate,
    cur_user: CurrentUser,
    ticket_service: TicketServiceDep
):
    assert cur_user.id is not None, "У пользователя из БД всегда есть ID"
    
    return await ticket_service.create_ticket(ticket_in=ticket_in, creator_id=cur_user.id)


@router.get("/tickets")
async def get_all_tickets(
    cur_user: CurrentUser,
    ticket_service: TicketServiceDep,
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 15,
    target_creator_id: Annotated[int | None, Query(description="Фильтр по автору (только для админов)")] = None,
    target_agent_id: Annotated[int | None, Query(description="Фильтр по агенту (только для админов)")] = None,
    statuses: Annotated[List[Status] | None, Query()] = None,
    category_ids: Annotated[List[int] | None, Query()] = None,
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
    id: int,
    cur_user: CurrentUser,
    ticket_service: TicketServiceDep
):
    assert cur_user.id is not None, "У пользователя из БД всегда есть ID"
    
    raw_ticket = await ticket_service.get_ticket_by_id(id, cur_user)
    
    if cur_user.role in (Role.CLIENT, Role.AGENT):
        return TicketResponse.model_validate(raw_ticket)
    return TicketAdminResponse.model_validate(raw_ticket)


@router.patch("/tickets/{id}/assign")
async def assign_ticket(
    ticket_service: TicketServiceDep,
    id: int,
    staff_user: CurrentAgent,
    assign_id: Annotated[int | None, Body(embed=True)] = None,
):
    raw_ticket = await ticket_service.assign_ticket(id, staff_user, assign_id)
    
    if staff_user.role == Role.AGENT:
        return TicketResponse.model_validate(raw_ticket)
    
    return TicketAdminResponse.model_validate(raw_ticket)


@router.patch("/tickets/{id}/status")
async def update_ticket_status(
    id: int,
    update_data: TicketStatusUpdate,
    staff_user: CurrentAgent,
    ticket_service: TicketServiceDep
):
    raw_ticket = await ticket_service.update_ticket_status(id, staff_user, update_data.status)
    
    if staff_user.role == Role.AGENT:
        return TicketResponse.model_validate(raw_ticket)
    
    return TicketAdminResponse.model_validate(raw_ticket)


@router.patch("/tickets/{id}/description")
async def update_ticket_description(
    id: int,
    update_data: TicketDescriptionUpdate,
    user: CurrentUser,
    ticket_service: TicketServiceDep
):
    raw_ticket = await ticket_service.update_ticket_description(id, user, update_data.description)
    
    if user.role == Role.CLIENT:
        return TicketResponse.model_validate(raw_ticket)
    
    return TicketAdminResponse.model_validate(raw_ticket)


@router.patch("/tickets/{id}/priority")
async def update_ticket_priority(
    id: int,
    update_data: TicketPriorityUpdate,
    staff_user: CurrentAgent,
    ticket_service: TicketServiceDep
):
    raw_ticket = await ticket_service.update_ticket_priority(id, staff_user, update_data.priority)
    
    if staff_user.role == Role.AGENT:
        return TicketResponse.model_validate(raw_ticket)
    
    return TicketAdminResponse.model_validate(raw_ticket)


@router.get("/tickets/{id}/history", response_model=list[TicketHistoryResponse])
async def get_ticket_history(
    id: int,
    staff_user: CurrentAgent,
    ticket_service: TicketServiceDep
):
    return await ticket_service.get_ticket_history(id, staff_user)