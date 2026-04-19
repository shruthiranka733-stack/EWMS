import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

app = FastAPI(
    title='Export Workflow Management System (EWMS)',
    description='End-to-end workflow for India-to-US steel exports',
    version='1.0.0',
    docs_url='/api/docs',
    redoc_url='/api/redoc',
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:3000', 'http://localhost:8000'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.add_middleware(TrustedHostMiddleware, allowed_hosts=['localhost', '127.0.0.1'])

from app.middleware.error_handler import add_error_handler
from app.middleware.cache_middleware import CacheMiddleware
from app.routes import (
    shipments_router,
    documents_router,
    sales_invoices_router,
    tasks_router,
    accounting_router,
)
from app.routes import dd_risk, analytics, reports

app.add_middleware(CacheMiddleware)
add_error_handler(app)
app.include_router(shipments_router)
app.include_router(documents_router)
app.include_router(sales_invoices_router)
app.include_router(tasks_router)
app.include_router(accounting_router)
app.include_router(dd_risk.router)
app.include_router(analytics.router)
app.include_router(reports.router)


@app.get('/health')
async def health():
    return {'status': 'ok', 'service': 'ewms-api'}


@app.get('/')
async def root():
    return {'message': 'EWMS API is running', 'docs': '/api/docs'}


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(
        'app.main:app',
        host='0.0.0.0',
        port=8000,
        reload=os.getenv('ENVIRONMENT') == 'development',
    )
