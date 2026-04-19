'use client';

import { useEffect, useState } from 'react';
import { useAppStore } from '@/store/appStore';
import { shipmentAPI } from '@/services/api';
import NavigationBar from '@/components/organisms/NavigationBar';
import './dashboard.css';

interface Shipment {
  id: string;
  shipment_number: string;
  phase: string;
  shipment_status: string;
  invoice_count: number;
  created_at: string;
  sla_status?: string;
}

interface Stats {
  active: number;
  pending: number;
  completed: number;
  totalShipped: number;
}

export default function Dashboard() {
  const user = useAppStore((state) => state.user);
  const shipments = useAppStore((state) => state.shipments);
  const setShipments = useAppStore((state) => state.setShipments);
  const isLoading = useAppStore((state) => state.isLoading);
  const setIsLoading = useAppStore((state) => state.setIsLoading);

  const [stats, setStats] = useState<Stats>({
    active: 0,
    pending: 0,
    completed: 0,
    totalShipped: 0,
  });

  useEffect(() => {
    if (shipments.length > 0) {
      setStats({
        active: shipments.filter((s) => s.shipment_status === 'active').length,
        pending: shipments.filter((s) => s.phase === 'origin').length,
        completed: shipments.filter((s) => s.shipment_status === 'completed' || s.shipment_status === 'delivered').length,
        totalShipped: shipments.length,
      });
      return;
    }

    const fetchShipments = async () => {
      if (!user) return;
      setIsLoading(true);
      try {
        const response = await shipmentAPI.getAll(user.org_id);
        const data = response.data.shipments;
        setShipments(data);
        setStats({
          active: data.filter((s: Shipment) => s.shipment_status === 'active').length,
          pending: data.filter((s: Shipment) => s.phase === 'origin').length,
          completed: data.filter((s: Shipment) => s.shipment_status === 'completed').length,
          totalShipped: data.length,
        });
      } catch {
        // backend unavailable — mock data already in store
      } finally {
        setIsLoading(false);
      }
    };

    fetchShipments();
  }, [user, shipments, setShipments, setIsLoading]);

  const getStatusBg = (status: string) => {
    const map: Record<string, string> = {
      delivered: 'var(--st-delivered-bg)',
      intransit: 'var(--st-intransit-bg)',
      shipped: 'var(--st-shipped-bg)',
      pending: 'var(--st-pending-bg)',
      active: 'var(--st-intransit-bg)',
      cancelled: 'var(--st-canceled-bg)',
    };
    return map[status] || 'var(--st-shipped-bg)';
  };

  const getStatusFg = (status: string) => {
    const map: Record<string, string> = {
      delivered: 'var(--st-delivered-fg)',
      intransit: 'var(--st-intransit-fg)',
      shipped: 'var(--st-shipped-fg)',
      pending: 'var(--st-pending-fg)',
      active: 'var(--st-intransit-fg)',
      cancelled: 'var(--st-canceled-fg)',
    };
    return map[status] || 'var(--st-shipped-fg)';
  };

  return (
    <>
      <NavigationBar />
      <main className="dashboard-main">
        <div className="dashboard-container">
          <div className="dashboard-header">
            <h1>Dashboard</h1>
            <p className="dashboard-subtitle">Welcome back, {user?.name ?? 'User'}</p>
          </div>

          <div className="metrics-grid">
            <div className="metric-card">
              <div className="metric-label">Active Shipments</div>
              <div className="metric-value">{stats.active}</div>
              <div className="metric-change">+12%</div>
            </div>
            <div className="metric-card">
              <div className="metric-label">Pending Review</div>
              <div className="metric-value">{stats.pending}</div>
              <div className="metric-change">awaiting action</div>
            </div>
            <div className="metric-card">
              <div className="metric-label">Completed</div>
              <div className="metric-value">{stats.completed}</div>
              <div className="metric-change">this month</div>
            </div>
            <div className="metric-card">
              <div className="metric-label">Total Shipped</div>
              <div className="metric-value">{stats.totalShipped}</div>
              <div className="metric-change">all time</div>
            </div>
          </div>

          <div className="shipments-section">
            <h2>Recent Shipments</h2>
            {isLoading ? (
              <div className="loading-state"><p>Loading shipments...</p></div>
            ) : shipments.length > 0 ? (
              <div className="shipments-list">
                {shipments.slice(0, 5).map((shipment) => (
                  <div key={shipment.id} className="shipment-row">
                    <div className="shipment-info">
                      <p className="shipment-number">{shipment.shipment_number}</p>
                      <p className="shipment-detail">{shipment.invoice_count} invoice(s) · {shipment.phase}</p>
                    </div>
                    <div className="shipment-meta">
                      <span
                        className="status-badge"
                        style={{
                          backgroundColor: getStatusBg(shipment.shipment_status),
                          color: getStatusFg(shipment.shipment_status),
                        }}
                      >
                        {shipment.shipment_status}
                      </span>
                      <button className="view-btn">View</button>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="empty-state"><p>No shipments yet</p></div>
            )}
          </div>
        </div>
      </main>
    </>
  );
}
