from fastapi import Depends
from ..schemas.user import User, UserCreate
from ..models.user import User as UserModel
import bcrypt
from sqlalchemy.orm import Session



def create_user(user_input: UserCreate,db:Session):
    db_user = UserModel(
        firstName=user_input.firstName,
        lastName=user_input.lastName,
        username=user_input.username,
        password = hash_password(user_input.password),
        dep_id = user_input.dep_id,
        role_id = user_input.role_id
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(user_id: int,db:Session):
    return db.query(UserModel).filter(UserModel.id == user_id).first()

def get_all_users(db:Session):
    return db.query(UserModel).all()

def hash_password(password: str):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password

def update_user_password(user_id: int, password: str, db: Session):
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if user:
        user.firstName = user.firstName
        user.lastName = user.lastName
        user.username = user.username
        user.password = hash_password(password)
        db.commit()
        db.refresh(user)
        return user
    return None

def delete_user(user_id:int, db: Session): 
    query = db.query(UserModel).filter(UserModel.id == user_id)
    user = query.first()
    if user:
        query.delete()
        db.commit()
        db.refresh(user)

        return  user
    
    return None


