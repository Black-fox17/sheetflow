from api.v1.models.base_model import BaseTableModel
from uuid_extensions import uuid7
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, text, Boolean, Index, ForeignKey, Numeric, ARRAY, ForeignKeyConstraint
from sqlalchemy.orm import foreign, remote

class Column(BaseTableModel):
    __tablename__ = "columns"
    template_id = Column(String, ForeignKey("templates.template_id"), nullable=False)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)  # e.g., 'text', 'date'
    required = Column(Boolean, default=False)
    sheet_no = Column(Numeric, nullable=False)
    
    # Add a composite foreign key constraint to link to Sheet
    __table_args__ = (
        ForeignKeyConstraint(
            ['template_id', 'sheet_no'],
            ['sheets.template_id', 'sheets.sheet_no']
        ),
    )

    template = relationship("Template", back_populates="columns")
    # Define a many-to-one relationship with Sheet
    sheet = relationship(
        "Sheet",
        back_populates="columns",
        foreign_keys=[template_id, sheet_no]
    )