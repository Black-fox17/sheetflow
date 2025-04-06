from pydantic import BaseModel
from typing import Dict, Any, Optional

class RowCreate(BaseModel):
    """Schema to create a row"""
    template_id: str
    sheet_no: int
    row_number: int
    data: Dict[str, Any]

class RowUpdate(BaseModel):
    """Schema to update a row"""
    data: Dict[str, Any]

class RowResponse(BaseModel):
    """Schema for row response"""
    row_id: str
    template_id: str
    sheet_no: int
    row_number: int
    data: Dict[str, Any]
    created_at: Optional[str] = None
    updated_at: Optional[str] = None 