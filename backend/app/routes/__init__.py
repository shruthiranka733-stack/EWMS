from .shipments import router as shipments_router
from .documents import router as documents_router
from .sales_invoices import router as sales_invoices_router
from .tasks import router as tasks_router
from .accounting import router as accounting_router

__all__ = [
    'shipments_router',
    'documents_router',
    'sales_invoices_router',
    'tasks_router',
    'accounting_router',
]
