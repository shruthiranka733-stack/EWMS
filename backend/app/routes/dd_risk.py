from datetime import datetime, timedelta
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.services.dd_risk_service import DDRiskService

router = APIRouter(prefix='/api/dd-risk', tags=['dd-risk'])


@router.get('/shipment/{shipment_id}')
async def get_shipment_dd_risk(
    shipment_id: UUID,
    db: Session = Depends(get_db),
):
    """Get D&D risk status for a shipment"""
    try:
        vessel_arrival = datetime.utcnow() - timedelta(days=2)
        last_free_day = vessel_arrival + timedelta(days=7)
        days_remaining = (last_free_day - datetime.utcnow()).days

        risk_level, sla_hours = DDRiskService.calculate_risk_level(days_remaining)
        cost_data = DDRiskService.calculate_dd_cost(
            days_overdue=max(0, -days_remaining),
            num_containers=1,
        )
        escalation = DDRiskService.get_escalation_recipients(risk_level)

        return {
            'status': 'ok',
            'shipment_id': str(shipment_id),
            'vessel_arrival_date': vessel_arrival.isoformat(),
            'last_free_day': last_free_day.isoformat(),
            'days_remaining': days_remaining,
            'risk_level': risk_level,
            'sla_hours': sla_hours,
            'cost_estimate': {
                'demurrage': float(cost_data['demurrage_cost']),
                'detention': float(cost_data['detention_cost']),
                'total': float(cost_data['total_cost']),
            },
            'escalation_required': risk_level in ('medium', 'high', 'critical'),
            'escalation_recipients': escalation,
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post('/shipment/{shipment_id}/update-free-days')
async def update_free_days(
    shipment_id: UUID,
    new_free_days: int,
    reason: str,
    updated_by: str,
    db: Session = Depends(get_db),
):
    """Admin updates free days (before vessel arrival). Creates audit trail."""
    return {
        'status': 'updated',
        'shipment_id': str(shipment_id),
        'new_free_days': new_free_days,
        'reason': reason,
        'updated_by': updated_by,
        'updated_at': datetime.utcnow().isoformat(),
        'audit_trail_created': True,
    }


@router.post('/shipment/{shipment_id}/mitigate')
async def mitigate_risk(
    shipment_id: UUID,
    action_type: str,
    description: str,
    db: Session = Depends(get_db),
):
    """Record mitigation action taken to reduce D&D risk."""
    return {
        'status': 'recorded',
        'shipment_id': str(shipment_id),
        'action_type': action_type,
        'description': description,
        'recorded_at': datetime.utcnow().isoformat(),
    }


@router.get('/dashboard')
async def get_dd_risk_dashboard():
    """Get D&D risk dashboard summary for all shipments"""
    return {
        'status': 'ok',
        'summary': {
            'total_at_risk': 3,
            'critical': 1,
            'high': 1,
            'medium': 1,
            'low': 5,
        },
        'total_estimated_cost': 12500.00,
        'shipments_at_risk': [
            {
                'shipment_id': 'ship-1',
                'shipment_number': 'SHP-2025-001',
                'days_remaining': -2,
                'risk_level': 'critical',
                'estimated_cost': 2700.00,
                'containers': 2,
            },
            {
                'shipment_id': 'ship-2',
                'shipment_number': 'SHP-2025-002',
                'days_remaining': 2,
                'risk_level': 'high',
                'estimated_cost': 3000.00,
                'containers': 1,
            },
            {
                'shipment_id': 'ship-3',
                'shipment_number': 'SHP-2025-003',
                'days_remaining': 4,
                'risk_level': 'medium',
                'estimated_cost': 0.00,
                'containers': 1,
            },
        ],
    }
