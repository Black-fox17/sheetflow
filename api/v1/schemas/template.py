from pydantic import BaseModel
from typing import List

class Column(BaseModel):
    """Schema to create a column"""
    name: str
    type: str
    required: bool
    sheet_no: int

class Sheet(BaseModel):
    """Schema to create a sheet"""
    sheet_no: int
    sheet_name: str
    columns: List[Column]

class TemplateCreate(BaseModel):
    """Schema to create a template"""
    sheets: List[Sheet]
