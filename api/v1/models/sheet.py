from api.v1.models.base_model import BaseTableModel
from uuid_extensions import uuid7
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, text, Boolean, Index, ForeignKey, Numeric, ARRAY
from sqlalchemy.orm import foreign, remote

class Sheet(BaseTableModel):
    __tablename__ = "sheets"
    
    template_id = Column(String, ForeignKey("templates.template_id"), nullable=False)
    sheet_no = Column(Numeric, nullable=False)
    sheet_name = Column(String, nullable=False)

    template = relationship("Template", back_populates="sheets")
    # Define a one-to-many relationship with Column
    columns = relationship(
        "Column",
        back_populates="sheet",
        cascade="all, delete-orphan"
    )
    # Define a one-to-many relationship with Row
    rows = relationship(
        "Row",
        back_populates="sheet",
        cascade="all, delete-orphan"
    )
