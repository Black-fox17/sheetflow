from typing import Any, Optional, List, Dict
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import desc

from api.core.base.services import Service
from api.utils.db_validators import check_model_existence
from api.v1.models import Row, Sheet, Template, Column
from api.v1.schemas import row

class RowService(Service):
    """Row service"""
    
    def create(self, db: Session, schema: row.RowCreate):
        """Create a new row"""
        # Check if template exists
        template = db.query(Template).filter(Template.template_id == schema.template_id).first()
        if not template:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Template with ID {schema.template_id} not found"
            )
        
        # Check if sheet exists
        sheet = db.query(Sheet).filter(
            Sheet.template_id == schema.template_id,
            Sheet.sheet_no == schema.sheet_no
        ).first()
        
        if not sheet:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Sheet with number {schema.sheet_no} not found in template {schema.template_id}"
            )
        
        # Check if row number already exists
        existing_row = db.query(Row).filter(
            Row.template_id == schema.template_id,
            Row.sheet_no == schema.sheet_no,
            Row.row_number == schema.row_number
        ).first()
        
        if existing_row:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Row number {schema.row_number} already exists in sheet {schema.sheet_no}"
            )
        
        # Create new row
        new_row = Row(
            template_id=schema.template_id,
            sheet_no=schema.sheet_no,
            row_number=schema.row_number,
            data=schema.data
        )
        
        db.add(new_row)
        db.commit()
        db.refresh(new_row)
        
        return new_row
    
    def update(self, db: Session, row_id: str, schema: row.RowUpdate):
        """Update a row"""
        row = db.query(Row).filter(Row.row_id == row_id).first()
        if not row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Row with ID {row_id} not found"
            )
        
        # Update row data
        row.data = schema.data
        
        db.commit()
        db.refresh(row)
        
        return row
    
    def delete(self, db: Session, row_id: str):
        """Delete a row"""
        row = db.query(Row).filter(Row.row_id == row_id).first()
        if not row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Row with ID {row_id} not found"
            )
        
        db.delete(row)
        db.commit()
        
        return row

    def fetch(self, db: Session, template_id: str):
        """Fetch all rows for a template"""
        rows = db.query(Row).filter(Row.template_id == template_id).all()
        return rows
    
    def fetch_by_sheet(self, db: Session, template_id: str, sheet_no: int):
        """Fetch all rows for a sheet"""
        # Check if template exists
        template = db.query(Template).filter(Template.template_id == template_id).first()
        if not template:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Template with ID {template_id} not found"
            )
        
        # Check if sheet exists
        sheet = db.query(Sheet).filter(
            Sheet.template_id == template_id,
            Sheet.sheet_no == sheet_no
        ).first()
        
        if not sheet:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Sheet with number {sheet_no} not found in template {template_id}"
            )
        
        # Fetch all rows for the sheet
        rows = db.query(Row).filter(
            Row.template_id == template_id,
            Row.sheet_no == sheet_no
        ).order_by(Row.row_number).all()
        
        return rows
    
    def fetch_all(self):
        return super().fetch_all()

row_service = RowService() 