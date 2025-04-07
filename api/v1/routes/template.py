from typing import Annotated, Optional, Literal
from fastapi import Depends, APIRouter, status, HTTPException
from sqlalchemy.orm import Session
from api.utils.success_response import success_response
from api.v1.schemas import template
from api.v1.services.template import template_service
from api.db.database import get_db
template_router = APIRouter(prefix="/templates", tags=["Templates"])

@template_router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_template(
    template_data: template.TemplateCreate,
    db: Annotated[Session, Depends(get_db)]
):
    # Check if template data is provided
    if not template_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Template data is required"
        )
    # Check if sheets are provided
    if not template_data.sheets:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="At least one sheet is required"
        )

    # Validate sheet numbers are unique
    sheet_numbers = [sheet.sheet_no for sheet in template_data.sheets]
    if len(sheet_numbers) != len(set(sheet_numbers)):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Sheet numbers must be unique"
        )

    # Check if each sheet has columns
    for sheet in template_data.sheets:
        if not sheet.columns:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Sheet {sheet.sheet_name} must have at least one column"
            )

    try:
        created_template = template_service.create(db, template_data)
        return success_response(
            status_code=status.HTTP_201_CREATED,
            id=created_template, 
            message="Template created successfully"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
@template_router.get("/{template_id}", status_code=status.HTTP_200_OK)
async def get_template(
    template_id: str,
    db: Annotated[Session, Depends(get_db)]
):
    """Get a row by id"""
    try:
        row = template_service.fetch(db, template_id)
        return success_response(
            status_code=status.HTTP_200_OK,
            data=row,
            message="Row fetched successfully"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )