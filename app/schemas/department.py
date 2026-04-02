from pydantic import BaseModel, ConfigDict
from typing import Optional, List


class DepartmentBase(BaseModel):
    name: str
    domain: Optional[str] = None


class DepartmentCreate(DepartmentBase):
    pass  # All fields required


class DepartmentResponse(DepartmentBase):
    dep_id: int

    model_config = ConfigDict(from_attributes=True)


class DepartmentListResponse(BaseModel):
    departments: List[DepartmentResponse]

    model_config = ConfigDict(from_attributes=True)


class DepartmentUpdate(BaseModel):
    name: Optional[str] = None
    domain: Optional[str] = None
