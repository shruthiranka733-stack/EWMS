'use client';

import { useEffect, useState } from 'react';
import NavigationBar from '@/components/organisms/NavigationBar';
import api from '@/services/api';
import { BarChart, TrendingUp, Clock, Zap } from 'lucide-react';
import './analytics.css';

interface KPI {
  sla: { compliance_rate: number; on_track: number; breached: number };
  processing_time: { avg_hours: number; fastest: number; slowest: number };
  dd_risk: { total_estimated_cost: number; shipments_at_risk: number };
}

const MOCK_KPI: KPI = {
  sla: { compliance_rate: 66.7, on_track: 2, breached: 1 },
  processing_time: { avg_hours: 144, fastest: 144, slowest: 144 },
  dd_risk: { total_estimated_cost: 5700, shipments_at_risk: 3 },
};

export default function AnalyticsPage() {
  const [kpi, setKpi] = useState<KPI>(MOCK_KPI);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const fetchKPI = async () => {
      setLoading(true);
      try {
        const response = await api.get('/api/analytics/kpi-dashboard');
        setKpi({
          sla: response.data.sla,
          processing_time: response.data.processing_time,
          dd_risk: response.data.dd_risk,
        });
      } catch {
        // backend unavailable — mock data already set
      } finally {
        setLoading(false);
      }
    };
    fetchKPI();
  }, []);

  return (
    <>
      <NavigationBar />
      <main className="analytics-main">
        <div className="analytics-container">
          <h1>Analytics Dashboard</h1>
          <p className="subtitle">Key performance indicators and trends</p>

          <div className="kpi-grid">
            <div className="kpi-card">
              <div className="kpi-icon"><Zap size={24} /></div>
              <div className="kpi-content">
                <p className="kpi-label">SLA Compliance</p>
                <p className="kpi-value">{kpi.sla.compliance_rate}%</p>
                <p className="kpi-detail">{kpi.sla.on_track} on track · {kpi.sla.breached} breached</p>
              </div>
            </div>

            <div className="kpi-card">
              <div className="kpi-icon"><Clock size={24} /></div>
              <div className="kpi-content">
                <p className="kpi-label">Avg Processing Time</p>
                <p className="kpi-value">{kpi.processing_time.avg_hours}h</p>
                <p className="kpi-detail">Target: 24h</p>
              </div>
            </div>

            <div className="kpi-card">
              <div className="kpi-icon"><TrendingUp size={24} /></div>
              <div className="kpi-content">
                <p className="kpi-label">D&amp;D Estimated Cost</p>
                <p className="kpi-value">${kpi.dd_risk.total_estimated_cost.toLocaleString()}</p>
                <p className="kpi-detail">{kpi.dd_risk.shipments_at_risk} shipments at risk</p>
              </div>
            </div>

            <div className="kpi-card">
              <div className="kpi-icon"><BarChart size={24} /></div>
              <div className="kpi-content">
                <p className="kpi-label">Monthly Shipments</p>
                <p className="kpi-value">47</p>
                <p className="kpi-detail">↑ 8% vs last month</p>
              </div>
            </div>
          </div>

          <div className="charts-section">
            <h2>Trends</h2>
            <div className="chart-placeholder">
              <p>📊 Chart visualization coming in Week 6</p>
              <p>Integration with Recharts or Chart.js</p>
            </div>
          </div>
        </div>
      </main>
    </>
  );
}
