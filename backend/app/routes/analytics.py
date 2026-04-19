from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.services.analytics_service import AnalyticsService

router = APIRouter(prefix='/api/analytics', tags=['analytics'])

_MOCK_SHIPMENTS = [
    {'created_at': '2025-04-10T10:00:00Z', 'updated_at': '2025-04-18T10:00:00Z', 'sla_status': 'on_track'},
    {'created_at': '2025-04-12T14:00:00Z', 'updated_at': '2025-04-18T10:00:00Z', 'sla_status': 'on_track'},
    {'created_at': '2025-04-15T09:00:00Z', 'updated_at': '2025-04-18T10:00:00Z', 'sla_status': 'breached'},
]

_MOCK_DD_RISKS = [
    {'risk_level': 'critical', 'estimated_cost': 2700},
    {'risk_level': 'high', 'estimated_cost': 3000},
    {'risk_level': 'medium', 'estimated_cost': 0},
]


@router.get('/kpi-dashboard')
async def get_kpi_dashboard(
    org_id: str = None,
    db: Session = Depends(get_db),
):
    """Get KPI dashboard with all metrics"""
    try:
        return {
            'status': 'ok',
            'date_range': {'from': '2025-04-01', 'to': '2025-04-18'},
            'sla': AnalyticsService.calculate_sla_compliance(_MOCK_SHIPMENTS),
            'processing_time': AnalyticsService.calculate_processing_time(_MOCK_SHIPMENTS),
            'dd_risk': AnalyticsService.calculate_dd_metrics(_MOCK_DD_RISKS),
            'shipments': {'total': 3, 'active': 2, 'completed': 1},
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get('/trends')
async def get_trends(
    days: int = 30,
    db: Session = Depends(get_db),
):
    """Get shipment trends over time"""
    return {
        'status': 'ok',
        'days': days,
        'daily_shipments': [
            {'date': '2025-04-10', 'count': 2, 'sla_breached': 0},
            {'date': '2025-04-11', 'count': 3, 'sla_breached': 1},
            {'date': '2025-04-12', 'count': 1, 'sla_breached': 0},
        ],
        'cumulative_costs': [
            {'date': '2025-04-10', 'demurrage': 0, 'detention': 0},
            {'date': '2025-04-11', 'demurrage': 150, 'detention': 100},
            {'date': '2025-04-12', 'demurrage': 300, 'detention': 200},
        ],
    }
