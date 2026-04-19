'use client';

import { useEffect, useState } from 'react';
import NavigationBar from '@/components/organisms/NavigationBar';
import api from '@/services/api';
import { AlertTriangle, TrendingUp, DollarSign } from 'lucide-react';
import './dd-risk.css';

interface DDRisk {
  shipment_id: string;
  shipment_number: string;
  days_remaining: number;
  risk_level: string;
  estimated_cost: number;
  containers: number;
}

const MOCK_RISKS: DDRisk[] = [
  { shipment_id: 'ship-1', shipment_number: 'SHP-2025-001', days_remaining: -2, risk_level: 'critical', estimated_cost: 2700, containers: 2 },
  { shipment_id: 'ship-2', shipment_number: 'SHP-2025-002', days_remaining: 2, risk_level: 'high', estimated_cost: 3000, containers: 1 },
  { shipment_id: 'ship-3', shipment_number: 'SHP-2025-003', days_remaining: 4, risk_level: 'medium', estimated_cost: 0, containers: 1 },
];

const RISK_BG: Record<string, string> = {
  critical: 'var(--st-canceled-bg)',
  high: 'var(--st-pending-bg)',
  medium: 'var(--warning-soft)',
  low: 'var(--st-intransit-bg)',
};

const RISK_FG: Record<string, string> = {
  critical: 'var(--st-canceled-fg)',
  high: 'var(--st-pending-fg)',
  medium: 'var(--warning)',
  low: 'var(--st-intransit-fg)',
};

export default function DDRiskPage() {
  const [risks, setRisks] = useState<DDRisk[]>(MOCK_RISKS);
  const [summary, setSummary] = useState({ critical: 1, high: 1, medium: 1, total_cost: 12500 });
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      try {
        const response = await api.get('/api/dd-risk/dashboard');
        setRisks(response.data.shipments_at_risk);
        setSummary({
          critical: response.data.summary.critical,
          high: response.data.summary.high,
          medium: response.data.summary.medium,
          total_cost: response.data.total_estimated_cost,
        });
      } catch {
        // backend unavailable — mock data already set
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  return (
    <>
      <NavigationBar />
      <main className="dd-risk-main">
        <div className="dd-risk-container">
          <h1>D&amp;D Risk Management</h1>
          <p className="subtitle">Monitor demurrage &amp; detention risks and costs</p>

          <div className="risk-summary-grid">
            <div className="risk-card critical">
              <div className="icon"><AlertTriangle size={24} /></div>
              <div className="content">
                <p className="label">Critical</p>
                <p className="value">{summary.critical}</p>
              </div>
            </div>
            <div className="risk-card high">
              <div className="icon"><TrendingUp size={24} /></div>
              <div className="content">
                <p className="label">High Risk</p>
                <p className="value">{summary.high}</p>
              </div>
            </div>
            <div className="risk-card medium">
              <div className="icon"><AlertTriangle size={24} /></div>
              <div className="content">
                <p className="label">Medium Risk</p>
                <p className="value">{summary.medium}</p>
              </div>
            </div>
            <div className="risk-card cost">
              <div className="icon"><DollarSign size={24} /></div>
              <div className="content">
                <p className="label">Total Est. Cost</p>
                <p className="value">${summary.total_cost.toLocaleString()}</p>
              </div>
            </div>
          </div>

          <div className="shipments-at-risk">
            <h2>Shipments at Risk</h2>
            {loading ? (
              <p className="empty-state">Loading risks...</p>
            ) : (
              <div className="risk-list">
                {risks.map((risk) => (
                  <div key={risk.shipment_id} className="risk-item">
                    <div className="risk-header">
                      <h3>{risk.shipment_number}</h3>
                      <span
                        className="risk-badge"
                        style={{ backgroundColor: RISK_BG[risk.risk_level], color: RISK_FG[risk.risk_level] }}
                      >
                        {risk.risk_level}
                      </span>
                    </div>
                    <div className="risk-details">
                      <div className="detail">
                        <p className="label">Days Remaining</p>
                        <p className="value" style={{ color: risk.days_remaining < 0 ? 'var(--danger)' : 'var(--fg)' }}>
                          {risk.days_remaining < 0 ? `${Math.abs(risk.days_remaining)} overdue` : risk.days_remaining}
                        </p>
                      </div>
                      <div className="detail">
                        <p className="label">Containers</p>
                        <p className="value">{risk.containers}</p>
                      </div>
                      <div className="detail">
                        <p className="label">Est. Cost</p>
                        <p className="value">${risk.estimated_cost.toLocaleString()}</p>
                      </div>
                    </div>
                    <div className="risk-actions">
                      <button className="btn-primary">View Shipment</button>
                      <button className="btn-secondary">Mitigate</button>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </main>
    </>
  );
}
