from uuid import uuid4
from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Shipment(Base):
    __tablename__ = 'shipments'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    shipment_number = Column(String(50), unique=True)
    org_id = Column(UUID(as_uuid=True), ForeignKey('organizations.id'))
    phase = Column(String(50), default='origin')
    status = Column(String(50), default='active')
    invoice_ids = Column(ARRAY(UUID(as_uuid=True)), default=[])
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    organization = relationship('Organization', back_populates='shipments')
    documents = relationship('Document', back_populates='shipment')
    tasks = relationship('Task', back_populates='shipment')
