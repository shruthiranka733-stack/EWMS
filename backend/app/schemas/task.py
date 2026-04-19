from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID
from datetime import datetime


class TaskCreate(BaseModel):
    shipment_id: UUID = Field(description="ID of the associated shipment")
    task_type: str = Field(description="Type of task (e.g. document_review, customs_clearance)")
    assigned_to: UUID = Field(description="User ID of the assignee")
    due_at: datetime = Field(description="Deadline for task completion")
    priority: Optional[str] = Field(default="normal", description="Priority level (low, normal, high, urgent)")


class TaskUpdate(BaseModel):
    status: Optional[str] = Field(default=None, description="Task status (open, in_progress, completed, blocked)")
    assigned_to: Optional[UUID] = Field(default=None)
    due_at: Optional[datetime] = Field(default=None)
    priority: Optional[str] = Field(default=None)


class TaskResponse(BaseModel):
    id: UUID
    shipment_id: UUID
    task_type: str
    status: str
    assigned_to: UUID
    due_at: datetime
    created_at: datetime

    class Config:
        from_attributes = True
