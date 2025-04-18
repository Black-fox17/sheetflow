from fastapi import APIRouter
from api.v1.routes.template import template_router
from api.v1.routes.row import row_router

api_version_one = APIRouter(prefix="/api/v1")

api_version_one.include_router(template_router)
api_version_one.include_router(row_router)