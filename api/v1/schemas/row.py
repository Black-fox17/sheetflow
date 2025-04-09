from pydantic import BaseModel
from typing import Dict, Any, Optional, List

class RowCreate(BaseModel):
    """Schema to create a row"""
    template_id: Optional[str] = None
    sheet_no: int
    row_number: int
    data: Dict[str, Any]
class RowBatch(BaseModel):
    """Schema for what rows data look like"""
    data: Dict[str, Any]
    
class RowData(BaseModel):
    """Schema to create multiple rows"""
    template_id: str
    sheet_no: int
    rows: List[RowBatch]


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