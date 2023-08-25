from typing import List
from sqlalchemy.orm import Session

import models
from exceptions import UserInfoInfoAlreadyExistError, UserInfoNotFoundError
from models import UserInfo
from schemas import CreateAndUpdateUser
from _datetime import datetime,timedelta
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from typing import Annotated
from database import get_db

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
import requests
from requests.auth import HTTPBasicAuth




# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "asa"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
# Function to get list of user info
def get_all_users(session: Session, limit:int , offset: int) -> List[UserInfo]:
    return session.query(UserInfo).offset(offset).limit(limit).all()

def get_password_hash(password):
    return pwd_context.hash(password)
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Function to  get info of a particular user
def get_user_info_by_id(session: Session, _id: int) -> UserInfo:
    user_info = session.query(UserInfo).get(_id)
    # if user_info is None:
    #     raise UserInfoNotFoundError

    return user_info
def get_user_info_by_absence_id(session: Session, _id: int) :
    user_id = session.query(models.Absence).get(_id).user_id
    user_info = session.query(UserInfo).get(user_id)
    if user_info is None:
        raise UserInfoNotFoundError
    return user_info
def get_user_info_by_email(session: Session, _email: str) -> UserInfo:
    user_info = session.query(UserInfo).filter(UserInfo.email == _email).first()
    # user_info = session.query(UserInfo).get(2)
    if user_info is None:
        raise UserInfoNotFoundError
    return user_info
def authenticate_user(session: Session, email: str, pass_word: str)->UserInfo:
    user = get_user_info_by_email(session,email)
    print(user)
    if not user:
        return False
    if not verify_password(pass_word, user.pass_word):
        return False
    return user
# async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         username: str = payload.get("sub")
#         if username is None:
#             raise credentials_exception
#         token_data = TokenData(username=username)
#     except JWTError:
#         raise credentials_exception
#     user = get_user(fake_users_db, username=token_data.username)
#     if user is None:
#         raise credentials_exception
#     return user

# Function to add a new user info to the database
def create_user(session: Session, user_info: CreateAndUpdateUser) -> UserInfo:
    user_details = session.query(UserInfo).filter(UserInfo.email == user_info.email).first()
    if user_details is not None:
        raise UserInfoInfoAlreadyExistError
    user_info.pass_word =  get_password_hash(user_info.pass_word)

    new_user_info = UserInfo(**user_info.dict())
    session.add(new_user_info)
    session.commit()
    session.refresh(new_user_info)
    return new_user_info



# Function to update details of the user
def update_user_info(session: Session, _id: int, info_update: CreateAndUpdateUser) -> UserInfo:
    user_info = get_user_info_by_id(session, _id)

    if user_info is None:
        raise UserInfoNotFoundError

    user_info.name = info_update.name
    user_info.phone = info_update.phone
    # user_info.email = info_update.email
    user_info.pass_word = get_password_hash(info_update.pass_word)
    user_info.updated_at = datetime.now()


    session.commit()
    session.refresh(user_info)

    return user_info

# Function to delete a user info from the db
def delete_user_info(session: Session, _id: int):
    user_info = get_user_info_by_id(session, _id)

    if user_info is None:
        raise UserInfoNotFoundError

    session.delete(user_info)
    session.commit()

    return
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    # print(to_encode)
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt
def validate_token(token : Annotated[str, Depends(oauth2_scheme)],session : Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials,please come to Login page",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        email: str = payload.get("sub")
        # print(payload)
        if email is None :
            # requests.get("google.com")
            raise credentials_exception

    except JWTError :
        # requests.get("google.com")
        raise credentials_exception
    user = get_user_info_by_email(session, _email=email)
    # print(user.__dict__)
    return user
def get_all_user_by_manager(session: Session, _id: int) :
    print(_id)
    results = session.query(models.Manager_User.user_id).filter(models.Manager_User.manage_id == _id).all()
    all_user_id_by_manager = [value for value ,in results]

    return all_user_id_by_manager
def get_all_managers(session: Session) :
    results = session.query(models.UserInfo.id).filter(models.UserInfo.role_id == 2).all()
    all_manager_id = [value for value, in results]

    return all_manager_id