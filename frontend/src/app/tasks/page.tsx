'use client';

import { useAppStore } from '@/store/appStore';
import { formatDistanceToNow } from 'date-fns';

const TASK_LABELS: Record<string, string> = {
  review_sales_invoice_ocr:    'Review Invoice OCR',
  complete_packing_list:       'Complete Packing List',
  upload_real_bol:             'Upload Real BOL',
  select_invoices_for_shipment:'Select Invoices',
  fill_draft_bol_details:      'Fill Draft BOL',
};

function urgency(dueAt: string) {
  const h = (new Date(dueAt).getTime() - Date.now()) / 3_600_000;
  if (h < 0)  return 'overdue';
  if (h < 4)  return 'critical';
  if (h < 48) return 'high';
  return 'normal';
}

const BG: Record<string, string> = {
  overdue:  'var(--st-canceled-bg)',
  critical: 'var(--st-pending-bg)',
  high:     'var(--warning-soft)',
  normal:   'var(--st-intransit-bg)',
};
const FG: Record<string, string> = {
  overdue:  'var(--st-canceled-fg)',
  critical: 'var(--st-pending-fg)',
  high:     'var(--warning)',
  normal:   'var(--st-intransit-fg)',
};

export default function TasksPage() {
  const tasks = useAppStore((s) => s.tasks);
  const sorted = [...tasks].sort(
    (a, b) => new Date(a.due_at).getTime() - new Date(b.due_at).getTime()
  );

  return (
    <>
      <h1 className="page-title">Tasks</h1>
      <p className="page-subtitle">Your pending work items</p>

      <div className="card">
        {sorted.length === 0 ? (
          <p style={{ color: 'var(--fg-muted)', fontSize: 'var(--t-sm)' }}>No tasks assigned</p>
        ) : (
          <table className="data-table">
            <thead>
              <tr>
                <th>Task</th>
                <th>Due</th>
                <th>Priority</th>
                <th style={{ textAlign: 'right' }}>Action</th>
              </tr>
            </thead>
            <tbody>
              {sorted.map((task) => {
                const u = urgency(task.due_at);
                return (
                  <tr key={task.id}>
                    <td style={{ fontWeight: 'var(--w-semibold)' }}>
                      {TASK_LABELS[task.task_type] ?? task.task_type}
                    </td>
                    <td style={{ fontSize: 'var(--t-xs)', color: 'var(--fg-muted)' }}>
                      {formatDistanceToNow(new Date(task.due_at), { addSuffix: true })}
                    </td>
                    <td>
                      <span className="badge" style={{ background: BG[u], color: FG[u] }}>
                        {u}
                      </span>
                    </td>
                    <td style={{ textAlign: 'right' }}>
                      <button className="btn btn-sm btn-primary">Open</button>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        )}
      </div>
    </>
  );
}
