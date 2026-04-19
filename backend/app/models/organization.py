from uuid import uuid4
from datetime import datetime
from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Organization(Base):
    __tablename__ = 'organizations'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String(255))
    type = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow)

    users = relationship('User', back_populates='organization')
    shipments = relationship('Shipment', back_populates='organization')
