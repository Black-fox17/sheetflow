from api.v1.models.base_model import BaseTableModel
from uuid_extensions import uuid7
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, text, Boolean, Index, ForeignKey, Numeric, ARRAY

class Column(BaseTableModel):
    __tablename__ = "columns"
    template_id = Column(String, ForeignKey("templates.template_id"), nullable=False)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)  # e.g., 'text', 'date'
    required = Column(Boolean, default=False)
    sheet_no = Column(Numeric, nullable=False)

    template = relationship("Template", back_populates="columns")