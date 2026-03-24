from ..database import Base 
from sqlalchemy import Column, Integer, String  , DateTime
from sqlalchemy.orm import relationship 


class Task(Base): 
    __tablename__ = "tasks"
    task_id = Column(Integer,primary_key=True,index=True)
    name = Column(String)
    description = Column(String)
    created_at = Column(DateTime)
    created_from = relationship("users",back_populates="users.user_id") 
    assigned_to_dep = relationship("department",back_populates="department.id") 
    assigned_to_user = relationship("users",back_populates="users.user_id") 
    status = Column(String) 
    timestamp = Column(DateTime)