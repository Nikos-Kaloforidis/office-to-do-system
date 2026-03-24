from pydantic import BaseModel 
from typing import Optional
from datetime import datetime


class User(BaseModel):
    firstName: str
    lastName: str
    username: str
    dep_id: Optional[int] = None
    role_id: Optional[int] = None

class Department(BaseModel):
    name: str
    domain: Optional[str] = None

class Role(BaseModel):
    name: str
    description: Optional[str] = None
    admin_rights: bool = False
    dep_id: Optional[int] = None

class UserCreate(User): 
    password: str 

class UserUpdate(BaseModel):
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None
    dep_id: Optional[int] = None
    role_id: Optional[int] = None

class DepartmentUpdate(BaseModel):
    name: Optional[str] = None
    domain: Optional[str] = None

class RoleUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    admin_rights: Optional[bool] = None
    dep_id: Optional[int] = None
