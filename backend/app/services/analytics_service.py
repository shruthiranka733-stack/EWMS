from datetime import datetime


class AnalyticsService:
    """Calculate KPIs and metrics for the analytics dashboard."""

    @staticmethod
    def calculate_sla_compliance(shipments: list) -> dict:
        """Calculate SLA compliance percentage."""
        if not shipments:
            return {'compliance_rate': 100.0, 'on_track': 0, 'breached': 0, 'total': 0}

        total = len(shipments)
        breached = sum(1 for s in shipments if s.get('sla_status') == 'breached')
        compliance_rate = (total - breached) / total * 100

        return {
            'compliance_rate': round(compliance_rate, 1),
            'on_track': total - breached,
            'breached': breached,
            'total': total,
        }

    @staticmethod
    def calculate_processing_time(shipments: list) -> dict:
        """Calculate average processing time in hours."""
        if not shipments:
            return {'avg_hours': 0, 'fastest': 0, 'slowest': 0, 'samples': 0}

        times = []
        for s in shipments:
            try:
                created = datetime.fromisoformat(s['created_at'].replace('Z', '+00:00'))
                updated = datetime.fromisoformat(s['updated_at'].replace('Z', '+00:00'))
                times.append((updated - created).total_seconds() / 3600)
            except (KeyError, ValueError):
                continue

        if not times:
            return {'avg_hours': 0, 'fastest': 0, 'slowest': 0, 'samples': 0}

        return {
            'avg_hours': round(sum(times) / len(times), 1),
            'fastest': round(min(times), 1),
            'slowest': round(max(times), 1),
            'samples': len(times),
        }

    @staticmethod
    def calculate_dd_metrics(dd_risks: list) -> dict:
        """Calculate D&D risk and cost metrics."""
        total_cost = sum(r.get('estimated_cost', 0) for r in dd_risks)
        by_level = {
            level: sum(1 for r in dd_risks if r.get('risk_level') == level)
            for level in ('critical', 'high', 'medium', 'low')
        }

        return {
            'total_estimated_cost': total_cost,
            'shipments_at_risk': len(dd_risks),
            'by_risk_level': by_level,
            'avg_cost_per_shipment': round(total_cost / max(1, len(dd_risks)), 2),
        }
