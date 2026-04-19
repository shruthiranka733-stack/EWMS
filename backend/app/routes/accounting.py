from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from uuid import UUID
from app.config.database import get_db

router = APIRouter(prefix='/api/accounting', tags=['accounting'])


@router.post('/tickets')
async def create_accounting_ticket(
    db: Session = Depends(get_db),
):
    """Create accounting ticket"""
    return {'detail': 'Endpoint created, logic coming in Week 2'}


@router.get('/tickets/{ticket_id}')
async def get_ticket(
    ticket_id: UUID,
    db: Session = Depends(get_db),
):
    """Get accounting ticket"""
    return {'detail': 'Endpoint created, logic coming in Week 2'}


@router.get('/tickets')
async def list_tickets(
    org_id: UUID,
    db: Session = Depends(get_db),
):
    """List accounting tickets"""
    return []


@router.put('/tickets/{ticket_id}/post')
async def post_ticket(
    ticket_id: UUID,
    erp_voucher_number: str,
    db: Session = Depends(get_db),
):
    """Mark ticket as posted to ERP"""
    return {'status': 'posted'}
