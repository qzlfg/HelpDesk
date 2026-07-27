from typing import Annotated

from fastapi import APIRouter, Depends

from app.core.dependencies import get_current_admin, get_sla_service
from app.models.user import User
from app.schemas.sla_rule import CreateSLARule, SLARuleResponse, SLARuleUpdate
from app.services.sla_service import SLARuleService

router = APIRouter()


@router.get("/sla-rules", response_model=SLARuleResponse)
async def get_sla_rules(
    user: Annotated[User, Depends(get_current_admin)],
    sla_service: Annotated[SLARuleService, Depends(get_sla_service)]
):
    return await sla_service.get_all_active()


@router.post("/sla-rules", response_model=SLARuleResponse)
async def create_sla_rule(
    data_in: CreateSLARule,
    user: Annotated[User, Depends(get_current_admin)],
    sla_service: Annotated[SLARuleService, Depends(get_sla_service)]
):
    return await sla_service.create(data_in)


@router.patch("/sla_rules/{sla_id}", response_model=SLARuleResponse)
async def update_sla_rule(
    sla_id: int,
    update_in: SLARuleUpdate,
    user: Annotated[User, Depends(get_current_admin)],
    sla_service: Annotated[SLARuleService, Depends(get_sla_service)]
):
    return await sla_service.update(sla_id=sla_id, sla_update=update_in)

@router.delete("/sla_rules/{sla_id}", response_model=SLARuleResponse)
async def delete_sla_rule(
    sla_id: int,
    user: Annotated[User, Depends(get_current_admin)],
    sla_service: Annotated[SLARuleService, Depends(get_sla_service)]
):
    return await sla_service.delete_sla_rule(sla_id)