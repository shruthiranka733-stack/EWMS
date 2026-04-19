import { create } from 'zustand';

interface User {
  id: string;
  email: string;
  name: string;
  role: string;
  org_id: string;
}

interface Shipment {
  id: string;
  shipment_number: string;
  phase: string;
  shipment_status: string;
  invoice_count: number;
  created_at: string;
  sla_status?: string;
}

interface Invoice {
  id: string;
  invoice_number: string;
  exporter_name: string;
  buyer_name: string;
  total_value: number;
  currency: string;
  ocr_status: string;
  created_at: string;
}

interface Task {
  id: string;
  task_type: string;
  status: string;
  due_at: string;
  created_at: string;
}

interface AppState {
  user: User | null;
  setUser: (user: User | null) => void;
  shipments: Shipment[];
  setShipments: (shipments: Shipment[]) => void;
  invoices: Invoice[];
  setInvoices: (invoices: Invoice[]) => void;
  tasks: Task[];
  setTasks: (tasks: Task[]) => void;
  selectedShipmentId: string | null;
  setSelectedShipmentId: (id: string | null) => void;
  isLoading: boolean;
  setIsLoading: (loading: boolean) => void;
  error: string | null;
  setError: (error: string | null) => void;
}

export const useAppStore = create<AppState>((set) => ({
  user: null,
  setUser: (user) => set({ user }),
  shipments: [],
  setShipments: (shipments) => set({ shipments }),
  invoices: [],
  setInvoices: (invoices) => set({ invoices }),
  tasks: [],
  setTasks: (tasks) => set({ tasks }),
  selectedShipmentId: null,
  setSelectedShipmentId: (id) => set({ selectedShipmentId: id }),
  isLoading: false,
  setIsLoading: (loading) => set({ isLoading: loading }),
  error: null,
  setError: (error) => set({ error }),
}));
