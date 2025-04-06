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
from api.v1.models import Template, Sheet, Column
from api.v1.schemas import template
class TemplateService(Service):
    """Template service"""
    def generate_template_id(self):
        return ''.join(random.choices(string.ascii_letters + string.digits, k=10))
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
        """Fetch a template by id"""
        template = check_model_existence(db, Template, Template.template_id, template_id)
        return template

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