from fastapi import APIRouter

from src.services.lead_store import LeadRequest, create_lead, recent_leads

router = APIRouter(prefix="/leads", tags=["leads"])


@router.post("")
def post_lead(body: LeadRequest) -> dict:
    return create_lead(body)


@router.get("/recent")
def get_recent(limit: int = 20) -> list[dict]:
    return recent_leads(limit)
