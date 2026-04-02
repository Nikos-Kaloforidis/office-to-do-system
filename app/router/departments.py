from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..crud.department import (
    deleteDepartment,
    getAllDepartments,
    getDepartment,
    addDepartment,
    getEmployeesDepartment,
)
from ..schemas.department import (
    DepartmentResponse,
    DepartmentListResponse,
    DepartmentCreate,  # Updated schemas
)
from ..schemas.user import UserResponse
from ..database import get_db

department_router = APIRouter(
    prefix="/department",
    tags=["Department"],
    responses={404: {"description": "Not found"}},
)


@department_router.get("/show/all", response_model=DepartmentListResponse)
def showAllDepartments(db: Session = Depends(get_db)):
    departments = getAllDepartments(db)
    return {"departments": departments}


@department_router.get(
    "/show/{id}", status_code=status.HTTP_200_OK, response_model=DepartmentResponse
)
def showDepartment(id: int, db: Session = Depends(get_db)):
    department = getDepartment(dep_id=id, db=db)
    if not department:
        raise HTTPException(
            status_code=404, detail=f"Department with id {id} not found"
        )
    return department


@department_router.post(
    "/add", status_code=status.HTTP_201_CREATED, response_model=DepartmentResponse
)
def createDepartment(department_new: DepartmentCreate, db: Session = Depends(get_db)):
    new_dep = addDepartment(department_input=department_new, db=db)
    if not new_dep:
        raise HTTPException(status_code=400, detail="Could not create department")
    return new_dep


@department_router.delete("/remove/{id}", status_code=status.HTTP_204_NO_CONTENT)
def removeDepartment(id: int, db: Session = Depends(get_db)):
    success = deleteDepartment(dep_id=id, db=db)
    if not success:
        raise HTTPException(
            status_code=404, detail=f"Department with id {id} not found"
        )


@department_router.get("/all_users/{id}", response_model=List[UserResponse])
def getAllUsersFromDepartment(id: int, db: Session = Depends(get_db)):
    users = getEmployeesDepartment(id, db)
    if not users:
        raise HTTPException(
            status_code=404, detail="Department has no employees or not found"
        )
    return users
