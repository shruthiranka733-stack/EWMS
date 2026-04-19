'use client';

import { useState } from 'react';
import { X } from 'lucide-react';

interface ShipmentModalProps {
  shipmentId: string;
  open: boolean;
  onClose: () => void;
}

const TABS = ['overview', 'sla', 'documents', 'accounting'] as const;
type Tab = typeof TABS[number];

export default function ShipmentModal({ shipmentId, open, onClose }: ShipmentModalProps) {
  const [tab, setTab] = useState<Tab>('overview');

  if (!open) return null;

  const mock = {
    shipment_number: `SHP-2025-${shipmentId.slice(0, 5).toUpperCase()}`,
    phase: 'origin',
    status: 'active',
    invoice_count: 3,
    created_at: '2025-04-18',
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h2 className="modal-title">{mock.shipment_number}</h2>
          <button className="modal-close" onClick={onClose}><X size={18} /></button>
        </div>

        {/* Tabs */}
        <div style={{ display: 'flex', gap: 0, borderBottom: '1px solid var(--border)', marginBottom: 'var(--s-4)' }}>
          {TABS.map((t) => (
            <button
              key={t}
              onClick={() => setTab(t)}
              style={{
                padding: 'var(--s-3) var(--s-4)',
                background: 'none',
                border: 'none',
                borderBottom: tab === t ? '2px solid var(--brand-green)' : '2px solid transparent',
                color: tab === t ? 'var(--brand-green)' : 'var(--fg-muted)',
                cursor: 'pointer',
                fontSize: 'var(--t-sm)',
                fontWeight: tab === t ? 'var(--w-semibold)' : 'normal',
                textTransform: 'capitalize',
                fontFamily: 'inherit',
              }}
            >
              {t}
            </button>
          ))}
        </div>

        {tab === 'overview' && (
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 'var(--s-4)' }}>
            {[
              ['Phase', mock.phase],
              ['Status', mock.status],
              ['Invoices', String(mock.invoice_count)],
              ['Created', mock.created_at],
            ].map(([label, value]) => (
              <div key={label}>
                <p style={{ fontSize: 'var(--t-xs)', color: 'var(--fg-muted)', margin: '0 0 2px' }}>{label}</p>
                <p style={{ fontWeight: 'var(--w-semibold)', textTransform: 'capitalize', margin: 0 }}>{value}</p>
              </div>
            ))}
          </div>
        )}

        {tab !== 'overview' && (
          <p style={{ color: 'var(--fg-muted)', fontSize: 'var(--t-sm)' }}>
            {tab.charAt(0).toUpperCase() + tab.slice(1)} coming soon
          </p>
        )}

        <div style={{ display: 'flex', gap: 'var(--s-3)', marginTop: 'var(--s-6)' }}>
          <button className="btn btn-secondary" onClick={onClose}>Close</button>
          <button className="btn btn-primary">Edit Shipment</button>
        </div>
      </div>
    </div>
  );
}
