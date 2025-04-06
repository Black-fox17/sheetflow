from typing import Annotated, Optional, Literal
from fastapi import Depends, APIRouter, Request, status, Query, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from api.utils.success_response import success_response
from api.v1.schemas import template
from api.v1.services.template import template_service
from api.db.database import get_db

template_router = APIRouter(prefix="/templates", tags=["Templates"])

@template_router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_template(
    template: Annotated[template.TemplateCreate, Depends(template_service.create)],
    db: Annotated[Session, Depends(get_db)]
):
    template_service.create(db, template)
    return success_response(
        template_id=template.template_id,
        status_code=status.HTTP_201_CREATED,
        message="Template created successfully",
        data=template
    )
