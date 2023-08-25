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


# Function to get list of absence info
def get_all_absences(session: Session, limit: int, offset: int) -> List[models.Absence]:

    return session.query(models.Absence).offset(offset).limit(limit).all()


def get_all_absences_by_user_id(session: Session, limit: int, offset: int, user_id: int) -> List[models.Absence]:
    return session.query(models.Absence).filter(models.Absence.user_id == user_id).offset(offset).limit(limit).all()

def get_all_absences_by_manager_id(session: Session, user_id: int, limit: int, offset: int) -> List[models.Absence]:
    all_user_id_by_manager = services.crud.get_all_user_by_manager(session,user_id)
    return session.query(models.Absence).filter(models.Absence.user_id.in_(all_user_id_by_manager)).offset(offset).limit(limit).all()
def get_all_absences_for_admin(session: Session, limit: int, offset: int) -> List[models.Absence]:
    all_manager_id = services.crud.get_all_managers(session)
    return session.query(models.Absence).filter(models.Absence.user_id.in_(all_manager_id)).offset(offset).limit(limit).all()


# def get_password_hash(password):
#     return pwd_context.hash(password)
#
#
# def verify_password(plain_password, hashed_password):
#     return pwd_context.verify(plain_password, hashed_password)

# Function to  get info of a particular absence
def get_absence_info_by_id(session: Session, _id: int) -> models.Absence:
    absence_info = session.query(models.Absence).get(_id)
    if absence_info is None:
        raise exceptions.AbsenceInfoNotFoundError
    return absence_info


def create_absence(session: Session, absence_info: schemas.CreateAndUpdateAbsence, user_id: int) -> models.Absence:


    additional_absence_info = schemas.CreateAndUpdateAbsence(**absence_info.dict())
    additional_absence_info.user_id = user_id
    additional_absence_info.flag_allow = absence_info.flag_allow

    new_absence_info = models.Absence(**additional_absence_info.dict())
    session.add(new_absence_info)
    session.commit()
    session.refresh(new_absence_info)
    return new_absence_info


# Function to update details of the absence
def update_absence_info(
        session: Session,
        _id: int, accept_id: int,
        info_update: schemas.CreateAndUpdateAbsence,

) -> models.Absence:
    absence_info = get_absence_info_by_id(session, _id)
    if absence_info is None:
        raise exceptions.AbsenceNotFoundError
    # print(1231231,info_update)
    absence_info.accepted = info_update.accepted
    if info_update.accepted == 1 :
        user_info = services.crud.get_user_info_by_absence_id(session, _id)
        rest_allowed_day = user_info.rest_allowed_day
        register_days = absence_info.time_to - absence_info.time_from

        plus_hours = register_days.seconds / 60 / 60
        if plus_hours <= 4 and plus_hours >= 1:
            day_absence = register_days.days + 0.5
        elif plus_hours > 4:
            day_absence = register_days.days + 1
        else:
            day_absence = register_days.days
        if absence_info.flag_allow == 0 :
            day_absence = 0
        new_rest_allowed_day = rest_allowed_day - day_absence
        if new_rest_allowed_day < 0 :
            absence_info.accepted = 2
        user_info.rest_allowed_day = new_rest_allowed_day
    absence_info.accepted_at = datetime.now()
    absence_info.accept_id = accept_id
    session.commit()
    session.refresh(absence_info)
    print(absence_info.__dict__)
    return absence_info


# Function to delete a absence info from the db
def delete_absence_info(session: Session, _id: int):
    absence_info = get_absence_info_by_id(session, _id)

    if absence_info is None:
        raise exceptions.AbsenceNotFoundError

    session.delete(absence_info)
    session.commit()

    return
