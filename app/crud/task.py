from ..models.task import Task as TaskModel
from ..schemas.task import TaskCreate, TaskUpdate
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_


def get_task(db: Session, task_id: int):
    return db.query(TaskModel).filter(task_id == TaskModel.task_id).first()


def get_tasks(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = None,
    created_by_id: Optional[int] = None,
    assigned_user_id: Optional[int] = None,
    assigned_dep_id: Optional[int] = None,
) -> List[TaskModel]:
    """Get tasks with filters and relationships"""
    query = db.query(TaskModel)

    # Filters
    if status:
        query = query.filter(TaskModel.status == status)
    if created_by_id:
        query = query.filter(TaskModel.created_by_id == created_by_id)
    if assigned_user_id:
        query = query.filter(TaskModel.assigned_user_id == assigned_user_id)
    if assigned_dep_id:
        query = query.filter(TaskModel.assigned_dep_id == assigned_dep_id)

    return query.offset(skip).limit(limit).all()


def get_user_created_tasks(db: Session, user_id: int) -> List[TaskModel]:
    """Get tasks created or assigned to user"""
    return (
        db.query(TaskModel)
        .filter(
            TaskModel.created_by_id == user_id,
        )
        .all()
    )


def get_user_assigned_tasks(db: Session, user_id: int) -> List[TaskModel]:
    """Get tasks created or assigned to user"""
    return (
        db.query(TaskModel)
        .filter(
            TaskModel.assigned_user_id == user_id,
        )
        .all()
    )


def get_user_tasks_by_status(db: Session, status: str, user_id: int) -> List[TaskModel]:
    """Get tasks by status"""

    return (
        db.query(TaskModel)
        .filter(and_(TaskModel.status == status, TaskModel.assigned_user_id == user_id))
        .all()
    )


def get_department_tasks(db: Session, dep_id: int) -> List[TaskModel]:
    """Get tasks assigned to department"""
    return db.query(TaskModel).filter(TaskModel.assigned_dep_id == dep_id).all()


def delete_task(db: Session, task_id: int):
    query = db.query(TaskModel).filter(task_id == TaskModel.task_id)
    task_delete = query.first()
    if task_delete:
        query.delete()
        db.commit()

        return task_delete
    return None


def create_task(db: Session, task: TaskCreate) -> TaskModel:
    """Create new task"""
    task_data = task.model_dump()

    status_map = {
        "requested": "REQUESTED",
        "seen": "SEEN",
        "working": "WORKING",
        "completed": "COMPLETED",
    }
    task_data["status"] = status_map.get(task.status.value, "REQUESTED")

    db_task = TaskModel(**task_data)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def update_task(
    db: Session, task_id: int, task_update: TaskUpdate
) -> Optional[TaskModel]:
    db_task = db.query(TaskModel).filter(TaskModel.task_id == task_id).first()
    if not db_task:
        return None

    # Use model_dump for Pydantic v2 consistency
    update_data = task_update.model_dump(exclude_unset=True)

    # Handle Status Mapping (Crucial for DB consistency)
    if "status" in update_data and update_data["status"]:
        status_map = {
            "requested": "REQUESTED",
            "seen": "SEEN",
            "working": "WORKING",
            "completed": "COMPLETED",
        }

        # Get the value (handle if it's an Enum or raw string)
        val = update_data["status"]
        status_str = val.value if hasattr(val, "value") else str(val)

        # Update the dictionary with the uppercase version
        update_data["status"] = status_map.get(status_str.lower(), "REQUESTED")

    # Apply all updates
    for field, value in update_data.items():
        setattr(db_task, field, value)

    db.commit()
    db.refresh(db_task)
    return db_task


def count_tasks(db: Session) -> int:
    """Count total tasks"""
    return db.query(TaskModel).count()
