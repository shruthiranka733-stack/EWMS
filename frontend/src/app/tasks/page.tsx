'use client';

import { useEffect, useState } from 'react';
import { useAppStore } from '@/store/appStore';
import { taskAPI } from '@/services/api';
import NavigationBar from '@/components/organisms/NavigationBar';
import { formatDistanceToNow } from 'date-fns';
import './tasks.css';

interface Task {
  id: string;
  task_type: string;
  status: string;
  due_at: string;
  created_at: string;
}

const TASK_LABELS: Record<string, string> = {
  review_sales_invoice_ocr: 'Review Invoice OCR',
  complete_packing_list: 'Complete Packing List',
  upload_real_bol: 'Upload Real BOL',
  select_invoices_for_shipment: 'Select Invoices',
  fill_draft_bol_details: 'Fill BOL Details',
  generate_draft_bol: 'Generate Draft BOL',
};

type Urgency = 'overdue' | 'critical' | 'high' | 'normal';

function getUrgency(dueAt: string): Urgency {
  const msUntilDue = new Date(dueAt).getTime() - Date.now();
  const days = msUntilDue / (1000 * 60 * 60 * 24);
  if (days < 0) return 'overdue';
  if (days < 1) return 'critical';
  if (days < 3) return 'high';
  return 'normal';
}

const URGENCY_BG: Record<Urgency, string> = {
  overdue: 'var(--st-canceled-bg)',
  critical: 'var(--st-pending-bg)',
  high: 'var(--warning-soft)',
  normal: 'var(--st-intransit-bg)',
};

const URGENCY_FG: Record<Urgency, string> = {
  overdue: 'var(--st-canceled-fg)',
  critical: 'var(--st-pending-fg)',
  high: 'var(--warning)',
  normal: 'var(--st-intransit-fg)',
};

export default function TasksPage() {
  const user = useAppStore((state) => state.user);
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const fetchTasks = async () => {
      if (!user) return;
      setLoading(true);
      try {
        const response = await taskAPI.getAll({ assigned_to: user.id });
        const sorted = [...response.data.tasks].sort(
          (a: Task, b: Task) =>
            new Date(a.due_at).getTime() - new Date(b.due_at).getTime()
        );
        setTasks(sorted);
      } catch (error) {
        console.error('Failed to fetch tasks:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchTasks();
  }, [user]);

  const handleComplete = async (taskId: string) => {
    try {
      await taskAPI.complete(taskId);
      setTasks((prev) =>
        prev.map((t) => (t.id === taskId ? { ...t, status: 'completed' } : t))
      );
    } catch (error) {
      console.error('Failed to complete task:', error);
    }
  };

  return (
    <>
      <NavigationBar />
      <main className="tasks-main">
        <div className="tasks-container">
          <div className="tasks-header">
            <h1>My Tasks</h1>
            <span className="tasks-count">{tasks.filter((t) => t.status !== 'completed').length} open</span>
          </div>

          {loading ? (
            <div className="loading-state"><p>Loading tasks...</p></div>
          ) : tasks.length > 0 ? (
            <div className="tasks-list">
              {tasks.map((task) => {
                const urgency = getUrgency(task.due_at);
                const isCompleted = task.status === 'completed';
                return (
                  <div key={task.id} className={`task-card${isCompleted ? ' task-card--done' : ''}`}>
                    <div className="task-info">
                      <h3 className="task-title">
                        {TASK_LABELS[task.task_type] ?? task.task_type}
                      </h3>
                      <p className="task-due">
                        Due {formatDistanceToNow(new Date(task.due_at), { addSuffix: true })}
                      </p>
                    </div>
                    <div className="task-actions">
                      {!isCompleted && (
                        <span
                          className="urgency-badge"
                          style={{
                            backgroundColor: URGENCY_BG[urgency],
                            color: URGENCY_FG[urgency],
                          }}
                        >
                          {urgency}
                        </span>
                      )}
                      {isCompleted ? (
                        <span className="done-badge">Done</span>
                      ) : (
                        <button className="task-btn" onClick={() => handleComplete(task.id)}>
                          Complete
                        </button>
                      )}
                    </div>
                  </div>
                );
              })}
            </div>
          ) : (
            <div className="empty-state"><p>No tasks assigned</p></div>
          )}
        </div>
      </main>
    </>
  );
}
