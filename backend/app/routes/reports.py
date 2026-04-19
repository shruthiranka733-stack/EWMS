from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.services.report_service import ReportService

router = APIRouter(prefix='/api/reports', tags=['reports'])

_MOCK_TICKETS = [
    {'ticket_number': 'AE-001', 'trigger_event': 'Invoice', 'entry_type': 'Revenue', 'amount': 150000, 'status': 'posted'},
    {'ticket_number': 'AE-002', 'trigger_event': 'CHA Bill', 'entry_type': 'Expense', 'amount': 5000, 'status': 'posted'},
    {'ticket_number': 'AE-003', 'trigger_event': 'Ocean Freight', 'entry_type': 'Expense', 'amount': 8500, 'status': 'pending'},
]


@router.get('/shipment/{shipment_id}/pdf')
async def download_shipment_report(
    shipment_id: UUID,
    db: Session = Depends(get_db),
):
    """Download shipment report as PDF"""
    try:
        shipment_data = {
            'shipment_number': f'SHP-2025-{str(shipment_id)[:8].upper()}',
            'phase': 'origin',
            'status': 'active',
            'created_at': '2025-04-18',
            'invoice_count': 3,
        }
        pdf = ReportService.generate_shipment_report(shipment_data)
        return StreamingResponse(
            iter([pdf.getvalue()]),
            media_type='application/pdf',
            headers={'Content-Disposition': f'attachment; filename=shipment_{shipment_id}.pdf'},
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get('/accounting/pdf')
async def download_accounting_report(
    start_date: str = None,
    end_date: str = None,
    db: Session = Depends(get_db),
):
    """Download accounting report as PDF"""
    try:
        pdf = ReportService.generate_financial_report(_MOCK_TICKETS)
        return StreamingResponse(
            iter([pdf.getvalue()]),
            media_type='application/pdf',
            headers={'Content-Disposition': 'attachment; filename=accounting_report.pdf'},
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
