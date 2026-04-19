'use client';

import React from 'react';
import {
  BarChart, Bar, LineChart, Line, PieChart, Pie, Cell,
  XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer,
} from 'recharts';
import styles from './chart-dashboard.module.css';

const MONTHLY_SHIPMENTS = [
  { month: 'Oct', shipments: 12, completed: 10 },
  { month: 'Nov', shipments: 18, completed: 15 },
  { month: 'Dec', shipments: 14, completed: 12 },
  { month: 'Jan', shipments: 22, completed: 19 },
  { month: 'Feb', shipments: 25, completed: 22 },
  { month: 'Mar', shipments: 20, completed: 18 },
  { month: 'Apr', shipments: 28, completed: 24 },
];

const DD_COST_TREND = [
  { week: 'W1', cost: 4200 },
  { week: 'W2', cost: 3800 },
  { week: 'W3', cost: 5100 },
  { week: 'W4', cost: 4600 },
  { week: 'W5', cost: 2900 },
  { week: 'W6', cost: 3500 },
  { week: 'W7', cost: 2200 },
];

const RISK_DISTRIBUTION = [
  { name: 'Low', value: 42, color: '#22C55E' },
  { name: 'Medium', value: 28, color: '#F59E0B' },
  { name: 'High', value: 18, color: '#EF4444' },
  { name: 'Critical', value: 12, color: '#7C3AED' },
];

interface CustomTooltipProps {
  active?: boolean;
  payload?: Array<{ name: string; value: number; color: string }>;
  label?: string;
}

function CustomTooltip({ active, payload, label }: CustomTooltipProps) {
  if (!active || !payload?.length) return null;
  return (
    <div className={styles.tooltip}>
      {label && <p className={styles.tooltipLabel}>{label}</p>}
      {payload.map((p) => (
        <p key={p.name} style={{ color: p.color }}>
          {p.name}: <strong>{p.value}</strong>
        </p>
      ))}
    </div>
  );
}

export default function ChartDashboard() {
  return (
    <div className={styles.grid}>
      <div className={styles.card}>
        <h3 className={styles.cardTitle}>Monthly Shipments</h3>
        <ResponsiveContainer width="100%" height={240}>
          <BarChart data={MONTHLY_SHIPMENTS} margin={{ top: 8, right: 16, left: 0, bottom: 0 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="var(--n-100)" />
            <XAxis dataKey="month" tick={{ fontSize: 12, fill: 'var(--n-500)' }} />
            <YAxis tick={{ fontSize: 12, fill: 'var(--n-500)' }} />
            <Tooltip content={<CustomTooltip />} />
            <Legend wrapperStyle={{ fontSize: 12 }} />
            <Bar dataKey="shipments" name="Total" fill="var(--brand-green)" radius={[4, 4, 0, 0]} />
            <Bar dataKey="completed" name="Completed" fill="#86EFAC" radius={[4, 4, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>

      <div className={styles.card}>
        <h3 className={styles.cardTitle}>D&amp;D Cost Trend (Weekly)</h3>
        <ResponsiveContainer width="100%" height={240}>
          <LineChart data={DD_COST_TREND} margin={{ top: 8, right: 16, left: 0, bottom: 0 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="var(--n-100)" />
            <XAxis dataKey="week" tick={{ fontSize: 12, fill: 'var(--n-500)' }} />
            <YAxis tick={{ fontSize: 12, fill: 'var(--n-500)' }} tickFormatter={(v) => `$${v}`} />
            <Tooltip
              formatter={(v: number) => [`$${v.toLocaleString()}`, 'D&D Cost']}
              contentStyle={{ borderRadius: 8, border: '1px solid var(--n-200)' }}
            />
            <Line
              type="monotone"
              dataKey="cost"
              stroke="#EF4444"
              strokeWidth={2}
              dot={{ fill: '#EF4444', r: 4 }}
              activeDot={{ r: 6 }}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>

      <div className={styles.card}>
        <h3 className={styles.cardTitle}>Risk Distribution</h3>
        <div className={styles.pieWrapper}>
          <ResponsiveContainer width="60%" height={220}>
            <PieChart>
              <Pie
                data={RISK_DISTRIBUTION}
                cx="50%"
                cy="50%"
                innerRadius={55}
                outerRadius={90}
                paddingAngle={3}
                dataKey="value"
              >
                {RISK_DISTRIBUTION.map((entry) => (
                  <Cell key={entry.name} fill={entry.color} />
                ))}
              </Pie>
              <Tooltip formatter={(v: number) => [`${v}%`, 'Share']} />
            </PieChart>
          </ResponsiveContainer>
          <ul className={styles.legend}>
            {RISK_DISTRIBUTION.map((d) => (
              <li key={d.name} className={styles.legendItem}>
                <span className={styles.legendDot} style={{ background: d.color }} />
                <span>{d.name}</span>
                <strong>{d.value}%</strong>
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
}
