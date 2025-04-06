from api.v1.models.base_model import BaseTableModel
from uuid_extensions import uuid7
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, text, Boolean, Index, ForeignKey, Numeric, ARRAY

class Template(BaseTableModel):
    __tablename__ = "templates"
    template_id = Column(String, nullable=False, unique=True)
    
    sheets = relationship("Sheet", back_populates="template", cascade="all, delete-orphan")
    columns = relationship("Column", back_populates="template", cascade="all, delete-orphan")
