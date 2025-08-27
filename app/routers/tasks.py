from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional
from ..database import get_db
from ..models import Task, User
from ..schemas import TaskCreate, TaskOut, TaskUpdate
from ..deps import get_current_user

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.post("", response_model=TaskOut, status_code=201)
def create_task(payload: TaskCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    task = Task(**payload.model_dump(), owner_id=current_user.id)
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

@router.get("", response_model=List[TaskOut])
def list_tasks(
    status: Optional[str] = Query(default=None, description="Filter by status: pending|in_progress|done"),
    q: Optional[str] = Query(default=None, description="Search in title/description"),
    priority: Optional[int] = Query(default=None, ge=1, le=5),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=50, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = db.query(Task).filter(Task.owner_id == current_user.id)
    if status:
        query = query.filter(Task.status == status)
    if priority:
        query = query.filter(Task.priority == priority)
    if q:
        like = f"%{q}%"
        query = query.filter((Task.title.ilike(like)) | (Task.description.ilike(like)))
    return query.order_by(Task.created_at.desc()).offset(skip).limit(limit).all()

@router.get("/{task_id}", response_model=TaskOut)
def get_task(task_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    task = db.query(Task).filter(Task.id == task_id, Task.owner_id == current_user.id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.put("/{task_id}", response_model=TaskOut)
def update_task(task_id: int, payload: TaskCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    task = db.query(Task).filter(Task.id == task_id, Task.owner_id == current_user.id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    for k, v in payload.model_dump().items():
        setattr(task, k, v)
    db.commit()
    db.refresh(task)
    return task

@router.patch("/{task_id}", response_model=TaskOut)
def patch_task(task_id: int, payload: TaskUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    task = db.query(Task).filter(Task.id == task_id, Task.owner_id == current_user.id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(task, k, v)
    db.commit()
    db.refresh(task)
    return task

@router.delete("/{task_id}", status_code=204)
def delete_task(task_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    task = db.query(Task).filter(Task.id == task_id, Task.owner_id == current_user.id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
    return None
