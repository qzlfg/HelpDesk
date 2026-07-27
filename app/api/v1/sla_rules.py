from fastapi import APIRouter, Depends

from app.schemas.sla_rule import CreateSLARule, SLARuleUpdate, SLARuleResponse
from app.core.dependencies import get_sla_service, get_current_admin
from app.models.user import User
from app.services.sla_service import SLARuleService

router = APIRouter()


@router.get("/sla-rules", response_model=SLARuleResponse)
async def get_sla_rules(
    user: User = Depends(get_current_admin),
    sla_service: SLARuleService = Depends(get_sla_service)
):
    return await sla_service.get_all_active()