from uuid import uuid4
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Date, Numeric
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class SalesInvoice(Base):
    __tablename__ = 'sales_invoices'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    invoice_number = Column(String(50))
    exporter_name = Column(String(255))
    buyer_name = Column(String(255))
    invoice_date = Column(Date())
    total_value = Column(Numeric(12, 2))
    currency = Column(String(3))
    ocr_status = Column(String(50), default='pending_hitl')
    created_at = Column(DateTime, default=datetime.utcnow)
