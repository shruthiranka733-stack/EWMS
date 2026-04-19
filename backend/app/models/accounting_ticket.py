from uuid import uuid4
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Numeric, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class AccountingTicket(Base):
    __tablename__ = 'accounting_tickets'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    shipment_id = Column(UUID(as_uuid=True), ForeignKey('shipments.id'))
    ticket_number = Column(String(50), unique=True)
    trigger_event = Column(String(100))
    entry_type = Column(String(50))
    amount = Column(Numeric(12, 2))
    currency = Column(String(3))
    status = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow)

    shipment = relationship('Shipment')
