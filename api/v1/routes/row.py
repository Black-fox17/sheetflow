from typing import Annotated, List
from fastapi import Depends, APIRouter, status, HTTPException
from sqlalchemy.orm import Session
from api.utils.success_response import success_response
from api.v1.schemas import row
from api.v1.services.row import row_service
from api.db.database import get_db

row_router = APIRouter(prefix="/rows", tags=["Rows"])

@row_router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_row(
    row_data: row.RowCreate,
    db: Annotated[Session, Depends(get_db)]
):
    """Create a new row"""
    try:
        created_row = row_service.create(db, row_data)
        return success_response(
            status_code=status.HTTP_201_CREATED,
            data=created_row,
            message="Row created successfully"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@row_router.put("/{row_id}", status_code=status.HTTP_200_OK)
async def update_row(
    row_id: str,
    row_data: row.RowUpdate,
    db: Annotated[Session, Depends(get_db)]
):
    """Update a row"""
    try:
        updated_row = row_service.update(db, row_id, row_data)
        return success_response(
            status_code=status.HTTP_200_OK,
            data=updated_row,
            message="Row updated successfully"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@row_router.delete("/{row_id}", status_code=status.HTTP_200_OK)
async def delete_row(
    row_id: str,
    db: Annotated[Session, Depends(get_db)]
):
    """Delete a row"""
    try:
        deleted_row = row_service.delete(db, row_id)
        return success_response(
            status_code=status.HTTP_200_OK,
            data=deleted_row,
            message="Row deleted successfully"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@row_router.get("/{row_id}", status_code=status.HTTP_200_OK)
async def get_row(
    row_id: str,
    db: Annotated[Session, Depends(get_db)]
):
    """Get a row by id"""
    try:
        row = row_service.fetch(db, row_id)
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

@row_router.get("/sheet/{template_id}/{sheet_no}", status_code=status.HTTP_200_OK)
async def get_rows_by_sheet(
    template_id: str,
    sheet_no: int,
    db: Annotated[Session, Depends(get_db)]
):
    """Get all rows for a sheet"""
    try:
        rows = row_service.fetch_by_sheet(db, template_id, sheet_no)
        return success_response(
            status_code=status.HTTP_200_OK,
            data=rows,
            message="Rows fetched successfully"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        ) 