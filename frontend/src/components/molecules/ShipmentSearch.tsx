'use client';

import React, { useState, useCallback } from 'react';
import styles from './shipment-search.module.css';

export interface SearchFilters {
  query: string;
  status: string;
  phase: string;
  dateFrom: string;
  dateTo: string;
}

interface ShipmentSearchProps {
  onSearch: (filters: SearchFilters) => void;
}

const STATUSES = ['', 'active', 'completed', 'on_hold', 'cancelled'];
const PHASES = ['', 'origin', 'transit', 'destination', 'customs', 'delivered'];

const EMPTY: SearchFilters = { query: '', status: '', phase: '', dateFrom: '', dateTo: '' };

export default function ShipmentSearch({ onSearch }: ShipmentSearchProps) {
  const [filters, setFilters] = useState<SearchFilters>(EMPTY);
  const [expanded, setExpanded] = useState(false);

  const set = useCallback((key: keyof SearchFilters, value: string) => {
    setFilters((prev) => {
      const next = { ...prev, [key]: value };
      onSearch(next);
      return next;
    });
  }, [onSearch]);

  const reset = () => {
    setFilters(EMPTY);
    onSearch(EMPTY);
  };

  const hasActive = Object.values(filters).some(Boolean);

  return (
    <div className={styles.wrapper}>
      <div className={styles.searchRow}>
        <div className={styles.inputWrap}>
          <svg className={styles.searchIcon} width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <circle cx="11" cy="11" r="8" /><path d="m21 21-4.35-4.35" />
          </svg>
          <input
            className={styles.input}
            type="text"
            placeholder="Search shipment number, origin, destination..."
            value={filters.query}
            onChange={(e) => set('query', e.target.value)}
          />
          {filters.query && (
            <button className={styles.clearBtn} onClick={() => set('query', '')} aria-label="Clear">×</button>
          )}
        </div>
        <button
          className={`${styles.filterToggle} ${expanded ? styles.active : ''}`}
          onClick={() => setExpanded((v) => !v)}
        >
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3" />
          </svg>
          Filters
          {hasActive && <span className={styles.badge} />}
        </button>
        {hasActive && (
          <button className={styles.resetBtn} onClick={reset}>Clear all</button>
        )}
      </div>

      {expanded && (
        <div className={styles.filterPanel}>
          <div className={styles.filterGroup}>
            <label className={styles.label}>Status</label>
            <select className={styles.select} value={filters.status} onChange={(e) => set('status', e.target.value)}>
              {STATUSES.map((s) => (
                <option key={s} value={s}>{s ? s.replace('_', ' ').replace(/\b\w/g, (c) => c.toUpperCase()) : 'All statuses'}</option>
              ))}
            </select>
          </div>
          <div className={styles.filterGroup}>
            <label className={styles.label}>Phase</label>
            <select className={styles.select} value={filters.phase} onChange={(e) => set('phase', e.target.value)}>
              {PHASES.map((p) => (
                <option key={p} value={p}>{p ? p.replace(/\b\w/g, (c) => c.toUpperCase()) : 'All phases'}</option>
              ))}
            </select>
          </div>
          <div className={styles.filterGroup}>
            <label className={styles.label}>Created From</label>
            <input
              className={styles.select}
              type="date"
              value={filters.dateFrom}
              onChange={(e) => set('dateFrom', e.target.value)}
            />
          </div>
          <div className={styles.filterGroup}>
            <label className={styles.label}>Created To</label>
            <input
              className={styles.select}
              type="date"
              value={filters.dateTo}
              onChange={(e) => set('dateTo', e.target.value)}
            />
          </div>
        </div>
      )}
    </div>
  );
}
