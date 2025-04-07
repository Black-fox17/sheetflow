import random
import string
from typing import Any, Optional, Annotated
import datetime as dt
from fastapi import status
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import desc


from api.core.base.services import Service
from api.db.database import get_db

from api.utils.db_validators import check_model_existence
from api.v1.models import Template, Sheet, Column, Row  
from api.v1.schemas import template
from uuid_extensions import uuid7
class TemplateService(Service):
    """Template service"""
    def generate_template_id(self):
        return str(uuid7())
    def create(self,db: Session, schema: template.TemplateCreate):
        """Create a new template"""
        # Generate a unique template_id
        template_id = self.generate_template_id()
        
        # Check if template_id already exists (unlikely but possible)
        while db.query(Template).filter(Template.template_id == template_id).first():
            template_id = self.generate_template_id()
            
        template = Template(
            template_id=template_id,
        )
        db.add(template)
        for single_sheet in schema.sheets:
            sheet = Sheet(
                sheet_no=single_sheet.sheet_no,
                sheet_name=single_sheet.sheet_name,
                template_id=template.template_id,
            )
            db.add(sheet)
            for column in single_sheet.columns:
                column = Column(
                    template_id=template.template_id,
                    name=column.name,
                    type=column.type,
                    required=column.required,
                    sheet_no=single_sheet.sheet_no,
                )
                db.add(column)
        db.commit()
        db.refresh(template)
        return template
    def delete(self, db: Session, template_id: str):
        """Delete a template"""
        template = check_model_existence(db, Template, Template.template_id, template_id)
        db.delete(template)
        db.commit()
        return template

    def fetch(self, db: Session, template_id: str):
        """Fetch template data with sheets, columns, and rows in the format expected by the frontend"""
        # Check if template exists
        template = db.query(Template).filter(Template.template_id == template_id).first()
        if not template:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Template with ID {template_id} not found"
            )
        
        # Get all sheets for this template
        sheets = db.query(Sheet).filter(Sheet.template_id == template_id).order_by(Sheet.sheet_no).all()
        
        # Format the response
        formatted_sheets = []
        
        for sheet in sheets:
            # Get columns for this sheet
            columns = db.query(Column).filter(
                Column.template_id == template_id,
                Column.sheet_no == sheet.sheet_no
            ).all()
            
            # Format columns
            formatted_columns = []
            for column in columns:
                formatted_columns.append({
                    "id": column.name.lower().replace(" ", "_"),  # Create an ID from the column name
                    "name": column.name,
                    "type": column.type,
                    "required": column.required
                })
            
            # Get rows for this sheet
            rows = db.query(Row).filter(
                Row.template_id == template_id,
                Row.sheet_no == sheet.sheet_no
            ).order_by(Row.row_number).all()
            
            # Format rows
            formatted_rows = []
            for row in rows:
                formatted_rows.append(row.data)
            
            # Add sheet with its columns and rows
            formatted_sheets.append({
                "id": f"sheet{sheet.sheet_no}",
                "name": sheet.sheet_name,
                "columns": formatted_columns,
                "rows": formatted_rows
            })
        
        # Return the formatted data
        return {
            "id": template.template_id,
            "name": f"Template {template.template_id}",  # You might want to add a name field to your Template model
            "sheets": formatted_sheets,
            "createdAt": template.created_at.isoformat() if template.created_at else None,
            "lastModified": template.updated_at.isoformat() if template.updated_at else None
        }
    def fetch_all(self, db: Session):
        """Fetch all templates"""
        return db.query(Template).order_by(desc(Template.created_at)).all()

    def update(self, db: Session, template_id: str, schema: template.TemplateUpdate):
        """Update a template"""
        template = check_model_existence(db, Template, Template.template_id, template_id)
        for key, value in schema.dict(exclude_unset=True).items():
            setattr(template, key, value)
        db.commit()
        db.refresh(template)
        return template

template_service = TemplateService()