from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum
from ..schemas.user import User, Department  



class TaskStatus(str, Enum):
    REQUESTED = "requested"
    SEEN = "seen"
    WORKING = "working"
    COMPLETED = "completed"

class TaskBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    status: TaskStatus = TaskStatus.REQUESTED


class TaskCreate(TaskBase):
    created_by_id: int  # User ID who created
    assigned_user_id: Optional[int] = None  # User ID assigned to
    assigned_dep_id: Optional[int] = None   # Department ID
    timestamp: datetime = datetime.now()

class TaskUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    status: Optional[TaskStatus] = None
    assigned_user_id: Optional[int] = None
    assigned_dep_id: Optional[int] = None

class TaskResponse(TaskBase):
    task_id: int
    created_at: Optional[datetime] = None
    timestamp: Optional[datetime] = None
    
    created_by: User
    assigned_user: Optional[User] = None
    
    assigned_department: Optional[Department] = None

    class Config:
        from_attributes = True

class TaskList(BaseModel):
    tasks: List[TaskResponse]
    total: int
    page: int = 1
    limit: int = 10

    class Config:
        from_attributes = True
