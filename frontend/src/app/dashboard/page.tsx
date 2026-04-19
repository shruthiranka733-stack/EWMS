'use client';

import { useAppStore } from '@/store/appStore';

export default function Dashboard() {
  const user = useAppStore((s) => s.user);
  const shipments = useAppStore((s) => s.shipments);

  const active    = shipments.filter((s) => s.shipment_status === 'active').length;
  const pending   = shipments.filter((s) => s.shipment_status === 'pending').length;
  const completed = shipments.filter((s) => s.shipment_status === 'completed' || s.shipment_status === 'delivered').length;

  const statusBg: Record<string, string> = {
    active:    'var(--st-intransit-bg)',
    delivered: 'var(--st-delivered-bg)',
    completed: 'var(--st-delivered-bg)',
    pending:   'var(--st-pending-bg)',
  };
  const statusFg: Record<string, string> = {
    active:    'var(--st-intransit-fg)',
    delivered: 'var(--st-delivered-fg)',
    completed: 'var(--st-delivered-fg)',
    pending:   'var(--st-pending-fg)',
  };

  return (
    <>
      <h1 className="page-title">Dashboard</h1>
      <p className="page-subtitle">Welcome back, {user?.name ?? 'User'}</p>

      <div className="metrics-grid">
        <div className="card">
          <p className="card-title">Active</p>
          <p className="card-value">{active}</p>
          <p className="card-detail">In progress</p>
        </div>
        <div className="card">
          <p className="card-title">Pending</p>
          <p className="card-value">{pending}</p>
          <p className="card-detail">Awaiting review</p>
        </div>
        <div className="card">
          <p className="card-title">Completed</p>
          <p className="card-value">{completed}</p>
          <p className="card-detail">This month</p>
        </div>
        <div className="card">
          <p className="card-title">Total</p>
          <p className="card-value">{shipments.length}</p>
          <p className="card-detail">All time</p>
        </div>
      </div>

      <div className="card">
        <p className="card-title" style={{ marginBottom: 'var(--s-4)' }}>Recent Shipments</p>
        {shipments.length === 0 ? (
          <p style={{ color: 'var(--fg-muted)', fontSize: 'var(--t-sm)' }}>No shipments</p>
        ) : (
          <table className="data-table">
            <thead>
              <tr>
                <th>Shipment</th>
                <th>Phase</th>
                <th>Invoices</th>
                <th>Status</th>
                <th style={{ textAlign: 'right' }}>Action</th>
              </tr>
            </thead>
            <tbody>
              {shipments.map((s) => (
                <tr key={s.id}>
                  <td style={{ fontWeight: 'var(--w-semibold)', fontFamily: 'var(--font-mono)', fontSize: 'var(--t-xs)' }}>
                    {s.shipment_number}
                  </td>
                  <td style={{ textTransform: 'capitalize', fontSize: 'var(--t-xs)' }}>{s.phase}</td>
                  <td>{s.invoice_count}</td>
                  <td>
                    <span
                      className="badge"
                      style={{
                        background: statusBg[s.shipment_status] ?? 'var(--st-shipped-bg)',
                        color: statusFg[s.shipment_status] ?? 'var(--st-shipped-fg)',
                      }}
                    >
                      {s.shipment_status}
                    </span>
                  </td>
                  <td style={{ textAlign: 'right' }}>
                    <button className="btn btn-sm btn-primary">View</button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </>
  );
}
