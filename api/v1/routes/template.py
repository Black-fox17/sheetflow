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
    # Check if template data is provided
    if not template:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Template data is required"
        )

    # Check if sheets are provided
    if not template.sheets:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="At least one sheet is required"
        )

    # Validate sheet numbers are unique
    sheet_numbers = [sheet.sheet_no for sheet in template.sheets]
    if len(sheet_numbers) != len(set(sheet_numbers)):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Sheet numbers must be unique"
        )

    # Check if each sheet has columns
    for sheet in template.sheets:
        if not sheet.columns:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Sheet {sheet.sheet_name} must have at least one column"
            )

    try:
        created_template = template_service.create(db, template)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
    
    return success_response(
        template_id=created_template.template_id,
        status_code=status.HTTP_201_CREATED,
        message="Template created successfully",
        data=created_template
    )
