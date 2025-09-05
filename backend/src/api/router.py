from fastapi import APIRouter

from src.api.routes import leads, integrations

api_router = APIRouter()
api_router.include_router(leads.router)
api_router.include_router(integrations.router)

