'use client';

import React, { useState } from 'react';
import ChartDashboard from '@/components/organisms/ChartDashboard';
import ShipmentSearch, { SearchFilters } from '@/components/molecules/ShipmentSearch';
import styles from './advanced.module.css';

const MOCK_SHIPMENTS = [
  { id: '1', number: 'SHP-2025-00001', status: 'active', phase: 'origin', created: '2025-03-01', origin: 'Mumbai', destination: 'Houston' },
  { id: '2', number: 'SHP-2025-00002', status: 'completed', phase: 'delivered', created: '2025-02-15', origin: 'Chennai', destination: 'New York' },
  { id: '3', number: 'SHP-2025-00003', status: 'active', phase: 'transit', created: '2025-03-10', origin: 'Kolkata', destination: 'Los Angeles' },
  { id: '4', number: 'SHP-2025-00004', status: 'on_hold', phase: 'customs', created: '2025-03-18', origin: 'Mumbai', destination: 'Chicago' },
  { id: '5', number: 'SHP-2025-00005', status: 'active', phase: 'destination', created: '2025-04-01', origin: 'Nhava Sheva', destination: 'Seattle' },
];

type Shipment = typeof MOCK_SHIPMENTS[0];

function matchesFilters(s: Shipment, f: SearchFilters): boolean {
  if (f.query) {
    const q = f.query.toLowerCase();
    if (!s.number.toLowerCase().includes(q) &&
        !s.origin.toLowerCase().includes(q) &&
        !s.destination.toLowerCase().includes(q)) return false;
  }
  if (f.status && s.status !== f.status) return false;
  if (f.phase && s.phase !== f.phase) return false;
  if (f.dateFrom && s.created < f.dateFrom) return false;
  if (f.dateTo && s.created > f.dateTo) return false;
  return true;
}

export default function AdvancedAnalyticsPage() {
  const [filters, setFilters] = useState<SearchFilters>({ query: '', status: '', phase: '', dateFrom: '', dateTo: '' });

  const results = MOCK_SHIPMENTS.filter((s) => matchesFilters(s, filters));

  return (
    <main className={styles.page}>
      <header className={styles.header}>
        <div>
          <h1 className={styles.title}>Advanced Analytics</h1>
          <p className={styles.sub}>Interactive charts and shipment search</p>
        </div>
      </header>

      <section className={styles.section}>
        <ChartDashboard />
      </section>

      <section className={styles.section}>
        <h2 className={styles.sectionTitle}>Shipment Search</h2>
        <ShipmentSearch onSearch={setFilters} />

        <div className={styles.tableWrap}>
          <table className={styles.table}>
            <thead>
              <tr>
                <th>Shipment #</th>
                <th>Origin</th>
                <th>Destination</th>
                <th>Phase</th>
                <th>Status</th>
                <th>Created</th>
              </tr>
            </thead>
            <tbody>
              {results.length === 0 ? (
                <tr>
                  <td colSpan={6} className={styles.empty}>No shipments match your filters.</td>
                </tr>
              ) : results.map((s) => (
                <tr key={s.id}>
                  <td className={styles.mono}>{s.number}</td>
                  <td>{s.origin}</td>
                  <td>{s.destination}</td>
                  <td><span className={`${styles.badge} ${styles[s.phase]}`}>{s.phase}</span></td>
                  <td><span className={`${styles.badge} ${styles[s.status.replace('_', '')]}`}>{s.status.replace('_', ' ')}</span></td>
                  <td>{s.created}</td>
                </tr>
              ))}
            </tbody>
          </table>
          <p className={styles.count}>{results.length} of {MOCK_SHIPMENTS.length} shipments</p>
        </div>
      </section>
    </main>
  );
}
