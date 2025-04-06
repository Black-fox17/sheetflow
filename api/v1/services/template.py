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
        if db.query(Template).filter(Template.template_id == schema.template_id).first():
            raise HTTPException(status_code=400, detail="Template with this template_id already exists")
        template = Template(
            template_id=self.generate_template_id(),
        )
        db.add(template)
        for sheet in schema.sheets:
            sheet = Sheet(
                sheet_no=sheet.sheet_no,
                sheet_name=sheet.sheet_name,
                template_id=template.template_id,
            )
            db.add(sheet)
            for column in sheet.columns:
                column = Column(
                    template_id=template.template_id,
                    name=column.name,
                    type=column.type,
                    required=column.required,
                    sheet_no=sheet.sheet_no,
                )
                db.add(column)
        db.commit()
        db.refresh(template)
        return template

template_service = TemplateService()