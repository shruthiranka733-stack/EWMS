from datetime import datetime
from uuid import UUID, uuid4

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.models import Task

router = APIRouter(prefix='/api/tasks', tags=['tasks'])


@router.post('', response_model=dict)
async def create_task(
    shipment_id: UUID,
    task_type: str,
    assigned_to: UUID,
    due_at: str,
    db: Session = Depends(get_db),
):
    """Create a new task"""
    try:
        task = Task(
            id=uuid4(),
            shipment_id=shipment_id,
            task_type=task_type,
            status='open',
            assigned_to=assigned_to,
            due_at=datetime.fromisoformat(due_at),
            created_at=datetime.utcnow(),
        )
        db.add(task)
        db.commit()

        return {
            'status': 'created',
            'task_id': str(task.id),
            'task_type': task.task_type,
            'due_at': task.due_at.isoformat(),
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@router.get('/{task_id}', response_model=dict)
async def get_task(
    task_id: UUID,
    db: Session = Depends(get_db),
):
    """Get task details"""
    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:
        raise HTTPException(status_code=404, detail='Task not found')

    return {
        'id': str(task.id),
        'task_type': task.task_type,
        'status': task.status,
        'due_at': task.due_at.isoformat() if task.due_at else None,
        'created_at': task.created_at.isoformat(),
    }


@router.get('', response_model=dict)
async def list_tasks(
    assigned_to: UUID = None,
    status: str = None,
    db: Session = Depends(get_db),
):
    """List tasks filtered by assigned_to and/or status"""
    query = db.query(Task)

    if assigned_to:
        query = query.filter(Task.assigned_to == assigned_to)
    if status:
        query = query.filter(Task.status == status)

    tasks = query.all()

    return {
        'count': len(tasks),
        'tasks': [
            {
                'id': str(t.id),
                'task_type': t.task_type,
                'status': t.status,
                'due_at': t.due_at.isoformat() if t.due_at else None,
                'created_at': t.created_at.isoformat(),
            }
            for t in tasks
        ],
    }


@router.put('/{task_id}', response_model=dict)
async def update_task(
    task_id: UUID,
    status: str = None,
    db: Session = Depends(get_db),
):
    """Update task status"""
    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:
        raise HTTPException(status_code=404, detail='Task not found')

    if status:
        task.status = status

    db.commit()

    return {
        'status': 'updated',
        'task_id': str(task.id),
        'task_status': task.status,
    }


@router.post('/{task_id}/complete', response_model=dict)
async def complete_task(
    task_id: UUID,
    db: Session = Depends(get_db),
):
    """Mark task as complete"""
    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:
        raise HTTPException(status_code=404, detail='Task not found')

    task.status = 'completed'
    db.commit()

    return {
        'status': 'completed',
        'task_id': str(task.id),
        'message': f'Task {task.task_type} completed',
    }
