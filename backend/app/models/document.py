from uuid import uuid4
from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Document(Base):
    __tablename__ = 'documents'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    shipment_id = Column(UUID(as_uuid=True), ForeignKey('shipments.id'))
    document_type = Column(String(50))
    status = Column(String(50))
    file_url = Column(String(500))
    created_at = Column(DateTime, default=datetime.utcnow)

    shipment = relationship('Shipment', back_populates='documents')
