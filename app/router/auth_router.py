
from fastapi import APIRouter,status,Response,Depends, HTTPException,Query
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from ..auth.jwt import authenticate_user
from ..auth.schemas import UserLogin
from ..database import get_db

router = APIRouter(tags=["Public"])

@router.post("/authenticate/")
def login(user:UserLogin, db:Session=Depends(get_db)): 
    token = authenticate_user(user_auth=user, db =db) 

    if  not token: 
        raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Incorrect username or password",
                    headers={"WWW-Authenticate": "Bearer"}, )   
                    
    return JSONResponse(status_code=status.HTTP_202_ACCEPTED,content=token)

