from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID
from datetime import datetime, date
from decimal import Decimal


class SalesInvoiceCreate(BaseModel):
    invoice_number: str = Field(description="Unique invoice number")
    exporter_name: str = Field(description="Name of the exporting company")
    buyer_name: str = Field(description="Name of the buyer")
    invoice_date: date = Field(description="Date the invoice was issued")
    total_value: Decimal = Field(description="Total invoice value")
    currency: str = Field(min_length=3, max_length=3, description="ISO 4217 currency code")


class SalesInvoiceUpdate(BaseModel):
    ocr_status: Optional[str] = Field(default=None, description="OCR processing status")
    ocr_data: Optional[dict] = Field(default=None, description="Raw OCR-extracted data")
    total_value: Optional[Decimal] = None
    currency: Optional[str] = Field(default=None, min_length=3, max_length=3)


class SalesInvoiceResponse(BaseModel):
    id: UUID
    invoice_number: str
    exporter_name: str
    buyer_name: str
    invoice_date: date
    total_value: Decimal
    currency: str
    ocr_status: str
    created_at: datetime

    class Config:
        from_attributes = True
