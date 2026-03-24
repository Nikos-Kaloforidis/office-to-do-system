from fastapi import APIRouter,status,Response,Depends
from sqlalchemy.orm import Session
from ..crud.user import get_user, create_user , get_all_users,delete_user,update_user_password
from ..schemas.user import User,UserCreate
from ..database import get_db

user_router = APIRouter(
    prefix="/users",
    tags=["Users"],
    responses= {404: {"description": "Not found"}},
)


@user_router.get("/show/all")
def showAllUsers(db:Session=Depends(get_db)):
    users = get_all_users(db)
    return users


@user_router.get("/show/{id}",status_code=status.HTTP_200_OK)
def showUser(id: int,db:Session=Depends(get_db)):
    user = get_user(id,db)
    if user:
        return user
    else:
        return Response(status_code=status.HTTP_404_NOT_FOUND, content=f"User with id {id} is not found")
    
@user_router.post("/create")
def addUser(user: UserCreate,db:Session=Depends(get_db)):
    new_user = create_user(user,db)
    return new_user

@user_router.delete("/remove")
def deleteUser(id:int, db:Session=Depends(get_db)): 
    user = delete_user(user_id = id ,db= db)
    if user: 
        return Response(status_code=status.HTTP_204_NO_CONTENT,content=f"User with id {id} deleted succesfully")
    else: 
        return Response(status_code=status.HTTP_404_NOT_FOUND, content=f"User with id {id} is not found")
    

@user_router.put("/update/password")
def updateUserPassword(id:int , password:str, db:Session=Depends(get_db)):
    user  = update_user_password(user_id=id,password=password, db = db)
    if user: 
        return Response(status_code=status.HTTP_202_ACCEPTED,content=f"User with id {id} updated succesfully")
    else:
        return Response(status_code=status.HTTP_404_NOT_FOUND, content=f"User with id {id} is not found")

@user_router.put("/update/admin_rights")
def updateUserAdminRights(): 
    pass
    




