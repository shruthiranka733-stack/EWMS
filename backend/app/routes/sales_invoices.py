from fastapi import APIRouter, Depends, File, UploadFile, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID, uuid4
from datetime import datetime, timedelta
from decimal import Decimal
from app.config.database import get_db
from app.models import SalesInvoice, Task
from app.services.mock_ocr_service import mock_ocr_service

router = APIRouter(prefix='/api/sales-invoices', tags=['sales-invoices'])


@router.post('/upload', response_model=dict)
async def upload_sales_invoice(
    org_id: UUID,
    file: UploadFile = File(...),
    uploaded_by_id: UUID = None,
    db: Session = Depends(get_db),
):
    """
    Upload Sales Invoice:
    1. Extract text via Mock OCR
    2. Create SalesInvoice entity with OCR data
    3. Create HITL review task
    4. Return invoice ID
    """
    try:
        ocr_data = await mock_ocr_service.extract_sales_invoice(file.filename)

        invoice = SalesInvoice(
            id=uuid4(),
            invoice_number=ocr_data['invoice_number'],
            exporter_name=ocr_data['exporter_name'],
            buyer_name=ocr_data['buyer_name'],
            invoice_date=ocr_data['invoice_date'],
            total_value=Decimal(str(ocr_data['total_value'])),
            currency=ocr_data['currency'],
            ocr_status='pending_hitl',
        )
        db.add(invoice)
        db.commit()

        hitl_task = Task(
            id=uuid4(),
            task_type='review_sales_invoice_ocr',
            status='open',
            assigned_to=None,
            due_at=datetime.utcnow() + timedelta(hours=24),
            shipment_id=None,
            created_at=datetime.utcnow(),
        )
        db.add(hitl_task)
        db.commit()

        return {
            'status': 'uploaded',
            'invoice_id': str(invoice.id),
            'invoice_number': invoice.invoice_number,
            'ocr_status': invoice.ocr_status,
            'total_value': float(invoice.total_value),
            'currency': invoice.currency,
            'message': f'Invoice {invoice.invoice_number} uploaded. Awaiting HITL review.',
        }

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f'Failed to upload invoice: {str(e)}')


@router.get('/{invoice_id}', response_model=dict)
async def get_sales_invoice(
    invoice_id: UUID,
    db: Session = Depends(get_db),
):
    """Get sales invoice details"""
    invoice = db.query(SalesInvoice).filter(SalesInvoice.id == invoice_id).first()

    if not invoice:
        raise HTTPException(status_code=404, detail='Invoice not found')

    return {
        'id': str(invoice.id),
        'invoice_number': invoice.invoice_number,
        'exporter_name': invoice.exporter_name,
        'buyer_name': invoice.buyer_name,
        'invoice_date': str(invoice.invoice_date),
        'total_value': float(invoice.total_value),
        'currency': invoice.currency,
        'ocr_status': invoice.ocr_status,
        'created_at': invoice.created_at.isoformat(),
    }


@router.get('', response_model=dict)
async def list_sales_invoices(
    org_id: UUID = None,
    ocr_status: str = None,
    db: Session = Depends(get_db),
):
    """List all sales invoices with optional filters"""
    query = db.query(SalesInvoice)

    if ocr_status:
        query = query.filter(SalesInvoice.ocr_status == ocr_status)

    invoices = query.all()

    return {
        'count': len(invoices),
        'invoices': [
            {
                'id': str(inv.id),
                'invoice_number': inv.invoice_number,
                'exporter_name': inv.exporter_name,
                'buyer_name': inv.buyer_name,
                'total_value': float(inv.total_value),
                'currency': inv.currency,
                'ocr_status': inv.ocr_status,
                'created_at': inv.created_at.isoformat(),
            }
            for inv in invoices
        ],
    }


@router.post('/{invoice_id}/approve-ocr', response_model=dict)
async def approve_invoice_ocr(
    invoice_id: UUID,
    feedback: str = None,
    approved_by_id: UUID = None,
    db: Session = Depends(get_db),
):
    """
    HITL approves Sales Invoice OCR.
    Triggers: Auto-generate 3 templates (PL, DDS, SSD)
    """
    try:
        invoice = db.query(SalesInvoice).filter(SalesInvoice.id == invoice_id).first()

        if not invoice:
            raise HTTPException(status_code=404, detail='Invoice not found')

        if invoice.ocr_status != 'pending_hitl':
            raise HTTPException(
                status_code=400,
                detail=f'Invoice status is {invoice.ocr_status}, not pending_hitl',
            )

        invoice.ocr_status = 'hitl_approved'
        db.commit()

        return {
            'status': 'approved',
            'invoice_id': str(invoice.id),
            'invoice_number': invoice.invoice_number,
            'message': 'Invoice OCR approved. 3 document templates auto-generated.',
            'auto_generated_docs': 3,
        }

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@router.post('/{invoice_id}/reject-ocr', response_model=dict)
async def reject_invoice_ocr(
    invoice_id: UUID,
    feedback: str,
    db: Session = Depends(get_db),
):
    """HITL rejects Sales Invoice OCR. User must re-upload."""
    try:
        invoice = db.query(SalesInvoice).filter(SalesInvoice.id == invoice_id).first()

        if not invoice:
            raise HTTPException(status_code=404, detail='Invoice not found')

        invoice.ocr_status = 'hitl_rejected'
        db.commit()

        return {
            'status': 'rejected',
            'invoice_id': str(invoice.id),
            'feedback': feedback,
            'message': 'Invoice OCR rejected. User notified to correct and resubmit.',
        }

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
