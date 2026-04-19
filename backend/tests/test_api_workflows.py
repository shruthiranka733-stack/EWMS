import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

# Patch DB engine creation before importing app so tests don't need a real DB
with patch('sqlalchemy.create_engine') as mock_engine:
    mock_engine.return_value = MagicMock()
    with patch('app.config.database.SessionLocal') as mock_session:
        from app.main import app

client = TestClient(app)


class TestHealthAndDocs:
    """Basic API availability tests"""

    def test_health_check(self):
        response = client.get('/health')
        assert response.status_code == 200
        assert response.json()['status'] == 'ok'

    def test_root_endpoint(self):
        response = client.get('/')
        assert response.status_code == 200
        assert 'message' in response.json()

    def test_swagger_docs_available(self):
        response = client.get('/api/docs')
        assert response.status_code == 200


class TestDDRiskEndpoints:
    """Test D&D risk API endpoints"""

    def test_dd_risk_dashboard(self):
        response = client.get('/api/dd-risk/dashboard')
        assert response.status_code == 200
        data = response.json()
        assert 'summary' in data
        assert 'shipments_at_risk' in data
        assert 'total_estimated_cost' in data

    def test_dd_risk_summary_structure(self):
        response = client.get('/api/dd-risk/dashboard')
        summary = response.json()['summary']
        assert 'critical' in summary
        assert 'high' in summary
        assert 'medium' in summary


class TestAnalyticsEndpoints:
    """Test analytics API endpoints"""

    def test_kpi_dashboard(self):
        response = client.get('/api/analytics/kpi-dashboard')
        assert response.status_code == 200
        data = response.json()
        assert 'sla' in data
        assert 'processing_time' in data
        assert 'dd_risk' in data

    def test_trends_endpoint(self):
        response = client.get('/api/analytics/trends')
        assert response.status_code == 200
        data = response.json()
        assert 'daily_shipments' in data
        assert 'cumulative_costs' in data

    def test_trends_custom_days(self):
        response = client.get('/api/analytics/trends?days=7')
        assert response.status_code == 200
        assert response.json()['days'] == 7
