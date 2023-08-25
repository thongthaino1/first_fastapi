from typing import List
import calendar
from sqlalchemy.orm import Session
from exceptions import WorkingInfoAlreadyExistError
import  exceptions
import models
import schemas
from _datetime import datetime,date,time,timedelta
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm


SECRET_KEY = "asa"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="sdfs")


# Function to get list of working info
# def get_all_workings(session: Session, limit: int, offset: int) -> List[models.Working]:
#     return session.query(models.Working).offset(offset).limit(limit).all()


def get_all_workings_by_user_id(session: Session,limit: int, offset: int, user_id: int) -> List[models.Working]:
    return session.query(models.Working).filter(models.Working.user_id == user_id).offset(offset).limit(limit).all()

def get_working_info_by_user_id(session: Session, user_id: int,today:date) -> models.Working:
    """

    :rtype: object
    """
    return session.query(models.Working).filter(models.Working.user_id == user_id,models.Working.workingDate == today).first()



# def get_password_hash(password):
#     return pwd_context.hash(password)
#
#
# def verify_password(plain_password, hashed_password):
#     return pwd_context.verify(plain_password, hashed_password)

# Function to  get info of a particular working
def get_working_info_by_id(session: Session, _id: int) -> models.Working:
    working_info = session.query(models.Working).get(_id)
    if working_info is None:
        raise exceptions.WorkingInfoNotFoundError
    return working_info


# def get_working_info_by_email(session: Session, _email: str) -> models.models.Working:
#     working_info = session.query(models.Working).filter(models.Working.email == _email).first()
#     # working_info = session.query(models.Working).get(2)
#     if working_info is None:
#         raise models.WorkingNotFoundError
#     return working_info


# def authenticate_working(session: Session, email: str, pass_word: str) -> models.Working:
#     abslseence = get_working_info_by_email(session, email)
#     print(verify_password(pass_word, working.pass_word))
#     if not working:
#         return False
#     if not verify_password(pass_word, working.pass_word):
#         return Fa
#     return working


def create_update_working(session: Session, user_id: int) -> models.Working:

    today = date.today()
    now = datetime.now()
    current_time = now.strftime("%H:%M")
    middle_time = "12:00:00"
    working_info = get_working_info_by_user_id(session,user_id ,today)


    if working_info is not None:
        a = working_info.checkinM if working_info.checkinM else None
        b = working_info.checkoutM if working_info.checkoutM else None
        c = working_info.checkinA if working_info.checkinA else None
        d = working_info.checkoutA if working_info.checkoutA else None
        if working_info and working_info.workingTime and a and b and c and d:
            return "Thong tin da ton tai"
        # print(working_info.checkinA)
        if middle_time > current_time :
            if working_info.checkinM :
                working_info.checkoutM = current_time
        else :
            if working_info.checkoutM and not working_info.checkinA:
                working_info.checkinA = current_time
            if working_info.checkinA and not working_info.checkoutA:
                working_info.checkoutA = current_time
        if a :
            a = datetime.strptime(str(a), '%H:%M')
        if b:
            b = datetime.strptime(str(b), '%H:%M')
        if c:
            c = datetime.strptime(str(c), '%H:%M')
        if d:
            d = datetime.strptime(str(d), '%H:%M')
        # print(a,b,c,d)
        if a and b and c and d :
            working_info.workingTime = str(d-c+b-a).split('.')[0]
        elif a and d :
            working_info.workingTime = str(d - a).split('.')[0]
        elif a and b:
            working_info.workingTime = str(b -a).split('.')[0]
        elif c and d :
            working_info.workingTime = str(d -c).split('.')[0]
        session.commit()
        session.refresh(working_info)
        return working_info
    else :
        working_info_create = schemas.CreateAndUpdateWorking()
        # print(middle_time,current_time)
        if middle_time > current_time:
            working_info_create.checkinM = current_time
        else :
            working_info_create.checkinA = current_time
        working_info_create.workingDate  = date.today()
        working_info_create.user_id = user_id
        new_working_info = models.Working(**working_info_create.dict())
        print(new_working_info)
        session.add(new_working_info)
        session.commit()
        session.refresh(new_working_info)
        return new_working_info


# Function to update details of the working
def update_working_info(session: Session,
                        user_id: int) -> models.Working:

    ...


# Function to delete a working info from the db
def delete_working_info(session: Session, _id: int):
    working_info = get_working_info_by_id(session, _id)

    if working_info is None:
        raise exceptions.WorkingNotFoundError

    session.delete(working_info)
    session.commit()

    return

def find_date_month_year(
        # current_user: Annotated[User, Depends(crud.validate_token)],
        # request: Request
):
    month = int(datetime.strftime(datetime.now(), "%m"))  # February
    year = int(datetime.strftime(datetime.now(), "%Y"))
    num_days = calendar.monthrange(year, month)[1]
    date = {"num_days":num_days,"year":year,"month":month}
    return date


