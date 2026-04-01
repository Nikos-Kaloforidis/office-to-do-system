from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..crud.user import get_user, create_user, get_all_users, delete_user, update_user_password, add_user_department
from ..schemas.user import (
    UserCreate, UserResponse, UserListResponse  # Updated schemas
)
from ..database import get_db
from ..auth.jwt import get_current_active_user
from ..models.user import User as UserModel

user_router = APIRouter(
    prefix="/users",
    tags=["Users"],
    responses={404: {"description": "Not found"}},
)

@user_router.get("/show/all", response_model=UserListResponse)
def showAllUsers(db: Session = Depends(get_db)):
    users = get_all_users(db)
    return {"users": users}

@user_router.get("/show/{id}", status_code=status.HTTP_200_OK, response_model=UserResponse)
def showUser(id: int, db: Session = Depends(get_db)):
    user = get_user(id, db)
    if not user:
        raise HTTPException(status_code=404, detail=f"User with id {id} is not found")
    return user

@user_router.post("/create", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def addUser(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(user, db)

@user_router.delete("/remove/{id}", status_code=status.HTTP_204_NO_CONTENT)
def deleteUser(id: int, db: Session = Depends(get_db)):
    success = delete_user(user_id=id, db=db)
    if not success:
        raise HTTPException(status_code=404, detail=f"User with id {id} is not found")

@user_router.put("/update/password/{id}", status_code=status.HTTP_200_OK, response_model=UserResponse)
def updateUserPassword(password_data : dict, db: Session = Depends(get_db)):
    id = password_data.get("id")
    password = password_data.get("password")
    if not password:
        raise HTTPException(status_code=422, detail="Password required")
    
    user = update_user_password(user_id=id, password=password, db=db)
    if not user:
        raise HTTPException(status_code=404, detail=f"User with id {id} is not found")
    return user

@user_router.put("/update/department/{id}/{dep_id}", status_code=status.HTTP_200_OK, response_model=UserResponse)
def update_department(id: int, dep_id: int, db: Session = Depends(get_db)):
    user = add_user_department(user_id=id, db=db, dep_id=dep_id)
    if not user:
        raise HTTPException(status_code=404, detail=f"User with id {id} is not found")
    return user

@user_router.get("/me", response_model=UserResponse)
def get_my_info(current_user: UserModel = Depends(get_current_active_user)):
    return current_user
