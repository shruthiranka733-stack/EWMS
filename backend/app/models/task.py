from uuid import uuid4
from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Task(Base):
    __tablename__ = 'tasks'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    shipment_id = Column(UUID(as_uuid=True), ForeignKey('shipments.id'))
    task_type = Column(String(100))
    status = Column(String(50), default='open')
    assigned_to = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    due_at = Column(DateTime())
    created_at = Column(DateTime, default=datetime.utcnow)

    shipment = relationship('Shipment', back_populates='tasks')
    assignee = relationship('User', back_populates='tasks')
