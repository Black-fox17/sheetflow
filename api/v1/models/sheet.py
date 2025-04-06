from api.v1.models.base_model import BaseTableModel
from uuid_extensions import uuid7
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, text, Boolean, Index, ForeignKey, Numeric, ARRAY

class Sheet(BaseTableModel):
    __tablename__ = "sheets"
    
    template_id = Column(String, ForeignKey("templates.template_id"), nullable=False)
    sheet_no = Column(Numeric, nullable=False)
    sheet_name = Column(String, nullable=False)

    template = relationship("Template", back_populates="sheets")
    columns = relationship("Column", back_populates="sheet", cascade="all, delete-orphan")
