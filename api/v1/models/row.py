from api.v1.models.base_model import BaseTableModel
from uuid_extensions import uuid7
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, text, Boolean, Index, ForeignKey, Numeric, ARRAY, ForeignKeyConstraint, JSON
from sqlalchemy.orm import foreign, remote

class Row(BaseTableModel):
    __tablename__ = "rows"
    
    row_id = Column(String, primary_key=True, default=lambda: str(uuid7()))
    template_id = Column(String, ForeignKey("templates.template_id"), nullable=False)
    sheet_no = Column(Numeric, nullable=False)
    row_number = Column(Numeric, nullable=False)
    data = Column(JSON, nullable=False)  # Store row data as JSON
    
    # Add a composite foreign key constraint to link to Sheet
    __table_args__ = (
        ForeignKeyConstraint(
            ['template_id', 'sheet_no'],
            ['sheets.template_id', 'sheets.sheet_no']
        ),
        # Ensure row numbers are unique within a sheet
        Index('ix_rows_template_sheet_row', 'template_id', 'sheet_no', 'row_number', unique=True)
    )

    template = relationship("Template", back_populates="rows")
    sheet = relationship(
        "Sheet",
        back_populates="rows",
        foreign_keys=[template_id, sheet_no]
    ) 