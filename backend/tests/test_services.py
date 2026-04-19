import pytest
from datetime import datetime, timedelta
from decimal import Decimal
from app.services.dd_risk_service import DDRiskService
from app.services.analytics_service import AnalyticsService


class TestDDRiskService:
    """Test D&D Risk Service calculations"""

    def test_risk_level_low(self):
        risk_level, sla = DDRiskService.calculate_risk_level(7)
        assert risk_level == 'low'
        assert sla is None

    def test_risk_level_medium(self):
        risk_level, sla = DDRiskService.calculate_risk_level(4)
        assert risk_level == 'medium'
        assert sla == 48

    def test_risk_level_high(self):
        risk_level, sla = DDRiskService.calculate_risk_level(2)
        assert risk_level == 'high'
        assert sla == 24

    def test_risk_level_critical(self):
        risk_level, sla = DDRiskService.calculate_risk_level(-1)
        assert risk_level == 'critical'
        assert sla == 4

    def test_dd_cost_zero_days(self):
        cost = DDRiskService.calculate_dd_cost(0, 1)
        assert cost['total_cost'] == Decimal('0')

    def test_dd_cost_positive_days(self):
        cost = DDRiskService.calculate_dd_cost(5, 2)
        assert cost['demurrage_cost'] == Decimal('150') * 5 * 2
        assert cost['detention_cost'] == Decimal('100') * 5 * 2
        assert cost['total_cost'] == cost['demurrage_cost'] + cost['detention_cost']

    def test_escalation_medium_risk(self):
        escalation = DDRiskService.get_escalation_recipients('medium')
        assert 'ops_manager@company.com' in escalation['email_recipients']
        assert 'email' in escalation['channels']

    def test_escalation_critical_risk(self):
        escalation = DDRiskService.get_escalation_recipients('critical')
        assert 'owner@company.com' in escalation['email_recipients']
        assert 'sms' in escalation['channels']
        assert 'slack' in escalation['channels']

    def test_escalation_low_risk_returns_empty(self):
        escalation = DDRiskService.get_escalation_recipients('low')
        assert escalation == {}


class TestAnalyticsService:
    """Test analytics calculations"""

    def test_sla_compliance_all_on_track(self):
        shipments = [{'sla_status': 'on_track'}, {'sla_status': 'on_track'}]
        result = AnalyticsService.calculate_sla_compliance(shipments)
        assert result['compliance_rate'] == 100.0

    def test_sla_compliance_with_breaches(self):
        shipments = [{'sla_status': 'on_track'}, {'sla_status': 'breached'}]
        result = AnalyticsService.calculate_sla_compliance(shipments)
        assert result['compliance_rate'] == 50.0
        assert result['breached'] == 1

    def test_sla_compliance_empty(self):
        result = AnalyticsService.calculate_sla_compliance([])
        assert result['compliance_rate'] == 100.0

    def test_processing_time_calculation(self):
        now = datetime.utcnow()
        shipments = [
            {'created_at': (now - timedelta(hours=24)).isoformat(), 'updated_at': now.isoformat()},
            {'created_at': (now - timedelta(hours=48)).isoformat(), 'updated_at': now.isoformat()},
        ]
        result = AnalyticsService.calculate_processing_time(shipments)
        assert result['avg_hours'] == 36.0
        assert result['fastest'] == 24.0
        assert result['slowest'] == 48.0

    def test_dd_metrics_calculation(self):
        risks = [
            {'risk_level': 'critical', 'estimated_cost': 2700},
            {'risk_level': 'high', 'estimated_cost': 3000},
            {'risk_level': 'medium', 'estimated_cost': 0},
        ]
        result = AnalyticsService.calculate_dd_metrics(risks)
        assert result['total_estimated_cost'] == 5700
        assert result['by_risk_level']['critical'] == 1
        assert result['by_risk_level']['high'] == 1
        assert result['shipments_at_risk'] == 3
