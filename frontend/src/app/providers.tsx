'use client';

import { useEffect } from 'react';
import { useAppStore } from '@/store/appStore';

const MOCK_USER = {
  id: '00000000-0000-0000-0000-000000000001',
  email: 'demo@ewms.com',
  name: 'Demo User',
  role: 'admin',
  org_id: '00000000-0000-0000-0000-000000000010',
};

const MOCK_SHIPMENTS = [
  { id: '1', shipment_number: 'SHP-2025-10042', phase: 'origin', shipment_status: 'active', invoice_count: 3, created_at: new Date().toISOString(), sla_status: 'on_track' },
  { id: '2', shipment_number: 'SHP-2025-10031', phase: 'transit', shipment_status: 'active', invoice_count: 1, created_at: new Date().toISOString(), sla_status: 'at_risk' },
  { id: '3', shipment_number: 'SHP-2025-09987', phase: 'destination', shipment_status: 'delivered', invoice_count: 2, created_at: new Date().toISOString(), sla_status: 'on_track' },
  { id: '4', shipment_number: 'SHP-2025-09801', phase: 'destination', shipment_status: 'completed', invoice_count: 4, created_at: new Date().toISOString(), sla_status: 'on_track' },
  { id: '5', shipment_number: 'SHP-2025-09654', phase: 'origin', shipment_status: 'pending', invoice_count: 2, created_at: new Date().toISOString(), sla_status: 'on_track' },
];

const MOCK_TASKS = [
  { id: '1', task_type: 'review_sales_invoice_ocr', status: 'open', due_at: new Date(Date.now() + 3600000 * 5).toISOString(), created_at: new Date().toISOString() },
  { id: '2', task_type: 'upload_real_bol', status: 'open', due_at: new Date(Date.now() + 3600000 * 48).toISOString(), created_at: new Date().toISOString() },
  { id: '3', task_type: 'complete_packing_list', status: 'open', due_at: new Date(Date.now() - 3600000 * 2).toISOString(), created_at: new Date().toISOString() },
  { id: '4', task_type: 'fill_draft_bol_details', status: 'open', due_at: new Date(Date.now() + 3600000 * 72).toISOString(), created_at: new Date().toISOString() },
];

export default function Providers({ children }: { children: React.ReactNode }) {
  const setUser = useAppStore((s) => s.setUser);
  const setShipments = useAppStore((s) => s.setShipments);
  const setTasks = useAppStore((s) => s.setTasks);

  useEffect(() => {
    setUser(MOCK_USER);
    setShipments(MOCK_SHIPMENTS);
    setTasks(MOCK_TASKS);
  }, [setUser, setShipments, setTasks]);

  return <>{children}</>;
}
