from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session
from uuid import UUID
from app.config.database import get_db
from app.schemas.document import DocumentCreate, DocumentResponse

router = APIRouter(prefix='/api/documents', tags=['documents'])


@router.post('/upload', response_model=DocumentResponse)
async def upload_document(
    shipment_id: UUID,
    document_type: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    """Upload a document"""
    return {'detail': 'Endpoint created, logic coming in Week 2'}


@router.get('/{document_id}', response_model=DocumentResponse)
async def get_document(
    document_id: UUID,
    db: Session = Depends(get_db),
):
    """Get document details"""
    return {'detail': 'Endpoint created, logic coming in Week 2'}


@router.get('', response_model=list)
async def list_documents(
    shipment_id: UUID,
    db: Session = Depends(get_db),
):
    """List documents for a shipment"""
    return []


@router.put('/{document_id}')
async def update_document(
    document_id: UUID,
    db: Session = Depends(get_db),
):
    """Update document"""
    return {'status': 'updated'}
