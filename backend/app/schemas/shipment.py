from pydantic import BaseModel, Field
from typing import List, Optional
from uuid import UUID
from datetime import datetime


class ShipmentCreate(BaseModel):
    invoice_ids: Optional[List[UUID]] = Field(default_factory=list, description="Invoices to club in this shipment")
    metadata: Optional[dict] = Field(default=None, description="Additional metadata")


class ShipmentUpdate(BaseModel):
    phase: Optional[str] = Field(default=None, description="Shipment phase (origin, transit, destination)")
    status: Optional[str] = Field(default=None, description="Shipment status (active, completed, cancelled)")


class ShipmentResponse(BaseModel):
    id: UUID
    shipment_number: str
    org_id: UUID
    phase: str
    status: str
    invoice_ids: List[UUID]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
