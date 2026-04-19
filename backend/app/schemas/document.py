from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID
from datetime import datetime


class DocumentCreate(BaseModel):
    shipment_id: UUID = Field(description="ID of the parent shipment")
    document_type: str = Field(description="Type of document (e.g. bill_of_lading, packing_list)")
    file_url: Optional[str] = Field(default=None, description="URL to the uploaded file")


class DocumentUpdate(BaseModel):
    status: Optional[str] = Field(default=None, description="Document status (draft, submitted, approved)")
    file_url: Optional[str] = Field(default=None)
    parsed_data: Optional[dict] = Field(default=None, description="OCR-parsed data from document")
    manual_entries: Optional[dict] = Field(default=None, description="Manually entered field overrides")


class DocumentResponse(BaseModel):
    id: UUID
    shipment_id: UUID
    document_type: str
    status: str
    file_url: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True
