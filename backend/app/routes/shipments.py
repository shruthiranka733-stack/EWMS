import random
import string
from datetime import datetime, timedelta
from uuid import UUID, uuid4

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.models import SalesInvoice, Shipment, SLATimeline, Task

router = APIRouter(prefix='/api/shipments', tags=['shipments'])


def generate_shipment_number() -> str:
    year = datetime.utcnow().year
    random_part = ''.join(random.choices(string.digits, k=5))
    return f'SHP-{year}-{random_part}'


@router.post('', response_model=dict)
async def create_shipment(
    org_id: UUID,
    invoice_ids: list = None,
    created_by_id: UUID = None,
    db: Session = Depends(get_db),
):
    """
    Create a shipment (two paths):
    Path A: User provides invoice_ids → auto-populates from approved invoices
    Path B: User creates empty → manual add later

    Creates initial SLA timeline for tracking.
    """
    try:
        if invoice_ids:
            for inv_id in invoice_ids:
                invoice = db.query(SalesInvoice).filter(SalesInvoice.id == inv_id).first()
                if not invoice:
                    raise HTTPException(status_code=404, detail=f'Invoice {inv_id} not found')
                if invoice.ocr_status != 'hitl_approved':
                    raise HTTPException(
                        status_code=400,
                        detail=f'Invoice {inv_id} not HITL-approved',
                    )

        shipment = Shipment(
            id=uuid4(),
            shipment_number=generate_shipment_number(),
            org_id=org_id,
            phase='origin',
            status='active',
            invoice_ids=invoice_ids or [],
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        db.add(shipment)
        db.commit()

        sla = SLATimeline(
            id=uuid4(),
            shipment_id=shipment.id,
            stage='invoice_approval',
            started_at=datetime.utcnow(),
            due_at=datetime.utcnow() + timedelta(hours=24),
            status='in_progress',
            created_at=datetime.utcnow(),
        )
        db.add(sla)

        task = Task(
            id=uuid4(),
            shipment_id=shipment.id,
            task_type='select_invoices_for_shipment',
            status='open',
            assigned_to=created_by_id,
            due_at=datetime.utcnow() + timedelta(hours=24),
            created_at=datetime.utcnow(),
        )
        db.add(task)
        db.commit()

        return {
            'status': 'created',
            'shipment_id': str(shipment.id),
            'shipment_number': shipment.shipment_number,
            'phase': shipment.phase,
            'shipment_status': shipment.status,
            'invoice_count': len(invoice_ids) if invoice_ids else 0,
            'message': f'Shipment {shipment.shipment_number} created successfully',
        }

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@router.get('/{shipment_id}', response_model=dict)
async def get_shipment(
    shipment_id: UUID,
    db: Session = Depends(get_db),
):
    """Get shipment details with SLA status"""
    shipment = db.query(Shipment).filter(Shipment.id == shipment_id).first()

    if not shipment:
        raise HTTPException(status_code=404, detail='Shipment not found')

    slas = db.query(SLATimeline).filter(SLATimeline.shipment_id == shipment_id).all()

    return {
        'id': str(shipment.id),
        'shipment_number': shipment.shipment_number,
        'phase': shipment.phase,
        'status': shipment.status,
        'invoice_ids': [str(inv_id) for inv_id in (shipment.invoice_ids or [])],
        'invoice_count': len(shipment.invoice_ids or []),
        'created_at': shipment.created_at.isoformat(),
        'updated_at': shipment.updated_at.isoformat(),
        'sla_count': len(slas),
        'sla_status': 'on_track' if all(s.status != 'breached' for s in slas) else 'breached',
    }


@router.get('', response_model=dict)
async def list_shipments(
    org_id: UUID,
    phase: str = None,
    status: str = None,
    db: Session = Depends(get_db),
):
    """List shipments with optional filters"""
    query = db.query(Shipment).filter(Shipment.org_id == org_id)

    if phase:
        query = query.filter(Shipment.phase == phase)
    if status:
        query = query.filter(Shipment.status == status)

    shipments = query.all()

    return {
        'count': len(shipments),
        'shipments': [
            {
                'id': str(s.id),
                'shipment_number': s.shipment_number,
                'phase': s.phase,
                'status': s.status,
                'invoice_count': len(s.invoice_ids or []),
                'created_at': s.created_at.isoformat(),
            }
            for s in shipments
        ],
    }


@router.put('/{shipment_id}', response_model=dict)
async def update_shipment(
    shipment_id: UUID,
    update_data: dict,
    db: Session = Depends(get_db),
):
    """Update shipment phase or status"""
    shipment = db.query(Shipment).filter(Shipment.id == shipment_id).first()

    if not shipment:
        raise HTTPException(status_code=404, detail='Shipment not found')

    if 'phase' in update_data:
        shipment.phase = update_data['phase']
    if 'status' in update_data:
        shipment.status = update_data['status']

    shipment.updated_at = datetime.utcnow()
    db.commit()

    return {
        'status': 'updated',
        'shipment_id': str(shipment.id),
        'phase': shipment.phase,
        'shipment_status': shipment.status,
    }


@router.delete('/{shipment_id}', response_model=dict)
async def delete_shipment(
    shipment_id: UUID,
    db: Session = Depends(get_db),
):
    """Cancel shipment"""
    shipment = db.query(Shipment).filter(Shipment.id == shipment_id).first()

    if not shipment:
        raise HTTPException(status_code=404, detail='Shipment not found')

    shipment.status = 'cancelled'
    db.commit()

    return {
        'status': 'cancelled',
        'shipment_id': str(shipment.id),
        'message': 'Shipment cancelled',
    }
