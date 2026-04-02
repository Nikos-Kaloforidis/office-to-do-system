from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from passlib.context import CryptContext
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from .schemas import UserLogin
from ..models.user import User as UserModel
from fastapi import HTTPException, status, Depends
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer
from ..database import get_db
import os

load_dotenv()

secret_key = os.getenv("SECRET_KEY")
algorithm = "HS256"
token_expire_minutes = 90

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


def hash_password(password: str):
    if len(password.encode()) > 72:
        password = password.encode()[:72].decode("utf-8", errors="ignore")
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(minutes=token_expire_minutes)

    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, secret_key, algorithm=algorithm)


def verify_access_token(token: str):
    try:
        return jwt.decode(token, secret_key, algorithms=[algorithm])
    except JWTError:
        return None


def authenticate_user(user_auth: UserLogin, db: Session):
    user = db.query(UserModel).filter(user_auth.username == UserModel.username).first()

    if not user:
        return None
    if not verify_password(user_auth.password, user.password):
        return None

    token_data = {"sub": user.username, "user_id": user.user_id}

    token = create_access_token(token_data)

    return {
        "access_token": token,
        "token_type": "bearer",
        "user_id": user.user_id,
        "username": user.username,
    }


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="authenticate/")


def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)
) -> UserModel:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = verify_access_token(token)
    if payload is None:
        raise credentials_exception
    username: str = payload.get("sub")
    if username is None:
        raise credentials_exception
    user = db.query(UserModel).filter(UserModel.username == username).first()
    if user is None:
        raise credentials_exception
    return user


def get_current_active_user(
    current_user: Annotated[UserModel, Depends(get_current_user)],
) -> UserModel:

    return current_user
