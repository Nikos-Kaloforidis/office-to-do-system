from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from enum import Enum as PyEnum
from sqlalchemy.dialects.postgresql import ENUM  # PostgreSQL specific
from ..database import Base 

from datetime  import datetime


class TaskStatus(PyEnum):
    REQUESTED = "requested"
    SEEN = "seen" 
    WORKING = "working"
    COMPLETED = "completed"

class Task(Base):
    __tablename__ = "tasks"
    
    task_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String)
    status = Column(ENUM(TaskStatus, name="task_status_enum"), default=TaskStatus.REQUESTED)
    created_at = Column(DateTime, default=datetime.now)
    timestamp = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    # Fix relationships (examples - adjust to your schema)
    created_by_id = Column(Integer, ForeignKey("users.user_id"))
    created_by = relationship("User", foreign_keys=[created_by_id], back_populates="created_tasks")
    
    assigned_dep_id = Column(Integer, ForeignKey("departments.dep_id"))
    assigned_department = relationship("Department", back_populates="tasks")
    
    assigned_user_id = Column(Integer, ForeignKey("users.user_id"))
    assigned_user = relationship("User", foreign_keys=[assigned_user_id], back_populates="assigned_tasks")

    # Usage: task.status = TaskStatus.WORKING
