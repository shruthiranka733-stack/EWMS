# EWMS API Documentation

## Base URL
`http://localhost:8000`

## Interactive Docs
Swagger UI: `http://localhost:8000/api/docs`
ReDoc:       `http://localhost:8000/api/redoc`

## Authentication
Phase 1: No auth required  
Phase 2: JWT Bearer tokens (planned)

---

## Endpoints

### Health
| Method | Path      | Description    |
|--------|-----------|----------------|
| GET    | /health   | Health check   |

### Shipments
| Method | Path                        | Description                  |
|--------|-----------------------------|------------------------------|
| GET    | /api/shipments              | List shipments (filter by org_id, phase, status) |
| POST   | /api/shipments              | Create shipment              |
| GET    | /api/shipments/{id}         | Get shipment + SLA status    |
| PUT    | /api/shipments/{id}         | Update phase/status          |
| DELETE | /api/shipments/{id}         | Cancel shipment              |

### Sales Invoices
| Method | Path                                   | Description               |
|--------|----------------------------------------|---------------------------|
| POST   | /api/sales-invoices/upload             | Upload + OCR extract      |
| GET    | /api/sales-invoices                    | List invoices             |
| GET    | /api/sales-invoices/{id}               | Get invoice details       |
| POST   | /api/sales-invoices/{id}/approve-ocr   | HITL approve              |
| POST   | /api/sales-invoices/{id}/reject-ocr    | HITL reject               |

### Documents
| Method | Path                        | Description               |
|--------|-----------------------------|---------------------------|
| POST   | /api/documents/upload       | Upload document           |
| GET    | /api/documents              | List docs for shipment    |
| GET    | /api/documents/{id}         | Get document              |
| PUT    | /api/documents/{id}         | Update document           |

### Tasks
| Method | Path                        | Description               |
|--------|-----------------------------|---------------------------|
| POST   | /api/tasks                  | Create task               |
| GET    | /api/tasks                  | List tasks (filter by assigned_to, status) |
| GET    | /api/tasks/{id}             | Get task                  |
| PUT    | /api/tasks/{id}             | Update status             |
| POST   | /api/tasks/{id}/complete    | Mark complete             |

### D&D Risk
| Method | Path                                          | Description               |
|--------|-----------------------------------------------|---------------------------|
| GET    | /api/dd-risk/dashboard                        | Risk summary (all ships)  |
| GET    | /api/dd-risk/shipment/{id}                    | Risk for one shipment     |
| POST   | /api/dd-risk/shipment/{id}/update-free-days   | Extend free days          |
| POST   | /api/dd-risk/shipment/{id}/mitigate           | Record mitigation         |

### Analytics
| Method | Path                            | Description               |
|--------|---------------------------------|---------------------------|
| GET    | /api/analytics/kpi-dashboard    | SLA, processing, D&D KPIs |
| GET    | /api/analytics/trends           | Daily shipment trends     |

### Accounting
| Method | Path                                  | Description               |
|--------|---------------------------------------|---------------------------|
| POST   | /api/accounting/tickets               | Create ticket             |
| GET    | /api/accounting/tickets               | List tickets              |
| GET    | /api/accounting/tickets/{id}          | Get ticket                |
| PUT    | /api/accounting/tickets/{id}/post     | Post to ERP               |
