from typing import List
from sqlalchemy.orm import Session
import exceptions

import models
import schemas
import services
from _datetime import datetime, date
import datetime as dt
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

SECRET_KEY = "asa"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="sdfs")


# Function to get list of add_wk info
def get_all_add_wks(session: Session, limit: int, offset: int) -> List[models.Add_WK]:

    return session.query(models.Add_WK).offset(offset).limit(limit).all()


def get_all_add_wks_by_user_id(session: Session, limit: int, offset: int, user_id: int) -> List[models.Add_WK]:
    return session.query(models.Add_WK).filter(models.Add_WK.user_id == user_id).offset(offset).limit(limit).all()

def get_all_add_wks_by_manager_id(session: Session, user_id: int, limit: int, offset: int) -> List[models.Add_WK]:
    all_user_id_by_manager = services.crud.get_all_user_by_manager(session,user_id)
    return session.query(models.Add_WK).filter(models.Add_WK.user_id.in_(all_user_id_by_manager)).offset(offset).limit(limit).all()
def get_all_add_wks_for_admin(session: Session, limit: int, offset: int) -> List[models.Add_WK]:
    all_manager_id = services.crud.get_all_managers(session)
    return session.query(models.Add_WK).filter(models.Add_WK.user_id.in_(all_manager_id)).offset(offset).limit(limit).all()

# def get_password_hash(password):
#     return pwd_context.hash(password)
#
#
# def verify_password(plain_password, hashed_password):
#     return pwd_context.verify(plain_password, hashed_password)

# Function to  get info of a particular add_wk
def get_add_wk_info_by_id(session: Session, _id: int) -> models.Add_WK:
    add_wk_info = session.query(models.Add_WK).get(_id)
    if add_wk_info is None:
        raise exceptions.Add_WKInfoNotFoundError
    return add_wk_info


def create_add_wk(session: Session, add_wk_info: schemas.CreateAndUpdateAdd_WK, user_id: int) -> models.Add_WK:


    additional_add_wk_info = schemas.CreateAndUpdateAdd_WK(**add_wk_info.dict())
    additional_add_wk_info.user_id = user_id
    additional_add_wk_info.flag_allow = add_wk_info.flag_allow

    new_add_wk_info = models.Add_WK(**additional_add_wk_info.dict())
    session.add(new_add_wk_info)
    session.commit()
    session.refresh(new_add_wk_info)
    return new_add_wk_info


# Function to update details of the add_wk
def update_add_wk_info(
        session: Session,
        _id: int, accept_id: int,
        info_update: schemas.CreateAndUpdateAdd_WK,

) -> models.Add_WK:
    add_wk_info = get_add_wk_info_by_id(session, _id)
    if add_wk_info is None:
        raise exceptions.Add_WKNotFoundError
    # print(1231231,info_update)
    add_wk_info.accepted = info_update.accepted
    add_wk_info.accepted_at = datetime.now()
    add_wk_info.accept_id = accept_id
    session.commit()
    session.refresh(add_wk_info)
    return add_wk_info


# Function to delete a add_wk info from the db
def delete_add_wk_info(session: Session, _id: int):
    add_wk_info = get_add_wk_info_by_id(session, _id)

    if add_wk_info is None:
        raise exceptions.Add_WKNotFoundError

    session.delete(add_wk_info)
    session.commit()

    return
