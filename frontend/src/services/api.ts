import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const invoiceAPI = {
  upload: (formData: FormData) =>
    api.post('/api/sales-invoices/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    }),
  getAll: (orgId: string) =>
    api.get('/api/sales-invoices', { params: { org_id: orgId } }),
  getOne: (invoiceId: string) =>
    api.get(`/api/sales-invoices/${invoiceId}`),
  approveOCR: (invoiceId: string, feedback?: string) =>
    api.post(`/api/sales-invoices/${invoiceId}/approve-ocr`, { feedback }),
  rejectOCR: (invoiceId: string, feedback: string) =>
    api.post(`/api/sales-invoices/${invoiceId}/reject-ocr`, { feedback }),
};

export const shipmentAPI = {
  create: (data: { org_id: string; invoice_ids?: string[] }) =>
    api.post('/api/shipments', data),
  getAll: (orgId: string, filters?: { phase?: string; status?: string }) =>
    api.get('/api/shipments', { params: { org_id: orgId, ...filters } }),
  getOne: (shipmentId: string) =>
    api.get(`/api/shipments/${shipmentId}`),
  update: (shipmentId: string, data: Record<string, unknown>) =>
    api.put(`/api/shipments/${shipmentId}`, data),
  delete: (shipmentId: string) =>
    api.delete(`/api/shipments/${shipmentId}`),
};

export const taskAPI = {
  create: (data: {
    shipment_id: string;
    task_type: string;
    assigned_to: string;
    due_at: string;
  }) =>
    api.post('/api/tasks', data),
  getAll: (filters?: { assigned_to?: string; status?: string }) =>
    api.get('/api/tasks', { params: filters }),
  getOne: (taskId: string) =>
    api.get(`/api/tasks/${taskId}`),
  update: (taskId: string, status: string) =>
    api.put(`/api/tasks/${taskId}`, { status }),
  complete: (taskId: string) =>
    api.post(`/api/tasks/${taskId}/complete`),
};

export const healthAPI = {
  check: () => api.get('/health'),
};

export default api;
