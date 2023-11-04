from fastapi import APIRouter

from routers.auth import api_router as auth_routers
# from routers.analyzer_model import api_router as analyzer_routers
from settings import api_settings

api_router = APIRouter(prefix=api_settings.URL)
api_router.include_router(auth_routers)
# api_router.include_router(analyzer_routers)
