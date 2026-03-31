from fastapi import APIRouter,status,Response,Depends, HTTPException,Query
from sqlalchemy.orm import Session
from typing import List, Optional
from ..crud.task import (
    get_task, get_tasks, create_task, update_task, delete_task, 
    count_tasks, get_department_tasks
)
from ..schemas.task import TaskCreate, TaskResponse, TaskList, TaskUpdate
from ..database import get_db

task_router = APIRouter(prefix="/tasks",
    tags=["Task"],
    responses= {404: {"description": "Not found"}},
)


@task_router.post("/", response_model=TaskResponse, status_code=201)
def create_new_task(task: TaskCreate, db: Session = Depends(get_db)):
    return create_task(db=db, task=task)

@task_router.get("/", response_model=TaskList)
def read_tasks(
    status: Optional[str] = Query(None, description="Filter by status"),
    skip: int = 0,
    limit: int = Query(100, le=100),
    db: Session = Depends(get_db)
):
    tasks = get_tasks(db, skip=skip, limit=limit, status=status)
    total = count_tasks(db)
    return TaskList(tasks=tasks, total=total)

@task_router.get("/{task_id}", response_model=TaskResponse)
def read_task(task_id: int, db: Session = Depends(get_db)):
    db_task = get_task(db, task_id=task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task

@task_router.patch("/{task_id}", response_model=TaskResponse)
def update_existing_task(
    task_id: int, 
    task_update: TaskUpdate, 
    db: Session = Depends(get_db)
):
    updated_task = update_task(db, task_id, task_update)
    if updated_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated_task

@task_router.delete("/{task_id}", status_code=204)
def delete_task_route(task_id: int, db: Session = Depends(get_db)):
    success = delete_task(db, task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return None

@task_router.get("/user/{user_id}")
def get_user_tasks(user_id: int, db: Session = Depends(get_db)):
    tasks = get_user_tasks(db, user_id)
    return {"tasks": tasks, "total": len(tasks)}

@task_router.get("/department/{dep_id}")
def get_user_tasks(dep_id: int, db: Session = Depends(get_db)):
    tasks = get_department_tasks(db, dep_id)
    return {"tasks": tasks, "total": len(tasks)}