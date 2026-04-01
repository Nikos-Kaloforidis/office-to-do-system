from pydantic import BaseModel, ConfigDict
from typing import Optional, List

class UserBase(BaseModel):
    firstName: str
    lastName: str
    username: str
    dep_id: Optional[int] = None

class UserCreate(UserBase):
    password: str

class UserResponse(UserCreate):
    user_id: int
    
    model_config = ConfigDict(from_attributes=True)  

class UserListResponse(BaseModel):
    users: List[UserResponse]
    
    model_config = ConfigDict(from_attributes=True)

class UserUpdate(BaseModel):
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None
    dep_id: Optional[int] = None
