from datetime import datetime, timedelta
from uuid import uuid4

from sqlalchemy.orm import Session

from app.models import SLATimeline


class SLAService:
    """Calculate SLA status, remaining time, and trigger alerts."""

    @staticmethod
    def calculate_sla_status(sla_timeline: SLATimeline) -> dict:
        """
        Calculate SLA timeline status and remaining time.

        Returns status as one of: on_track | at_risk | breached | completed
        """
        now = datetime.utcnow()

        if sla_timeline.status == 'completed':
            return {
                'status': 'completed',
                'hours_remaining': 0,
                'percentage_used': 100.0,
                'alert_level': 'info',
            }

        total_seconds = (sla_timeline.due_at - sla_timeline.started_at).total_seconds()
        elapsed_seconds = (now - sla_timeline.started_at).total_seconds()
        remaining_hours = (sla_timeline.due_at - now).total_seconds() / 3600

        percentage_used = (elapsed_seconds / total_seconds * 100) if total_seconds > 0 else 0

        if remaining_hours < 0:
            status, alert_level = 'breached', 'critical'
        elif percentage_used > 75:
            status, alert_level = 'at_risk', 'critical'
        elif percentage_used > 50:
            status, alert_level = 'at_risk', 'warning'
        else:
            status, alert_level = 'on_track', 'info'

        return {
            'status': status,
            'hours_remaining': max(0, int(remaining_hours)),
            'percentage_used': round(percentage_used, 1),
            'alert_level': alert_level,
        }

    @staticmethod
    def create_sla_timeline(
        shipment_id,
        stage: str,
        configured_hours: int = 24,
        db: Session = None,
    ) -> SLATimeline:
        """Create a new SLA timeline for a stage"""
        sla = SLATimeline(
            id=uuid4(),
            shipment_id=shipment_id,
            stage=stage,
            started_at=datetime.utcnow(),
            due_at=datetime.utcnow() + timedelta(hours=configured_hours),
            status='in_progress',
            created_at=datetime.utcnow(),
        )

        if db:
            db.add(sla)
            db.commit()

        return sla

    @staticmethod
    def check_and_update_sla_status(shipment_id, db: Session) -> None:
        """Check all SLA timelines for a shipment; mark breached if past due."""
        slas = db.query(SLATimeline).filter(
            SLATimeline.shipment_id == shipment_id,
            SLATimeline.status.in_(['pending', 'in_progress']),
        ).all()

        now = datetime.utcnow()
        for sla in slas:
            if now > sla.due_at:
                sla.status = 'breached'

        db.commit()
