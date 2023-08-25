from pydantic import BaseModel
from typing import Optional, List
from datetime import date, datetime, time, timedelta
# TO support creation and update APIs
class CreateAndUpdateUser(BaseModel):
    email: Optional[str] | None = None
    name: Optional[str]| None = None
    email_verified_at: Optional[datetime]| None = None
    phone: Optional[str]| None = None
    created_at: Optional[datetime]| None = None
    updated_at: Optional[datetime]| None = None
    pass_word : Optional[str] | None = None
    role_id : int | None = None
    rest_allowed_day : float | None = None

class CreateAndUpdateAbsence(BaseModel):
    user_id : Optional[int] | None = None
    accept_id: Optional[int] | None = None
    created_at: Optional[datetime] | None = None
    accepted_at: Optional[datetime] | None = None
    reason: Optional[str] | None = None
    flag_allow: Optional[int] | None = None
    time_from: Optional[datetime] | None = None
    time_to: Optional[datetime] | None = None
    accepted: Optional[int] | None = None

class CreateAndUpdateAdd_WK(BaseModel):
    user_id: Optional[int] | None = None
    accept_id: Optional[int] | None = None
    created_at: Optional[datetime] | None = None
    accepted_at: Optional[datetime] | None = None
    reason: Optional[str] | None = None
    flag_allow: Optional[int] | None = None
    time_from: Optional[datetime] | None = None
    time_to: Optional[datetime] | None = None
    accepted: Optional[int] | None = None



class CreateAndUpdateWorking(BaseModel):

    user_id : Optional[int] = None
    workingDate : Optional[date] = None
    checkinA : Optional[time]| None = None
    checkinM : Optional[time]| None = None
    checkinA : Optional[time]| None = None
    checkoutA : Optional[time]| None = None
    workingTime : Optional[time]| None = None

class Working(CreateAndUpdateWorking):
    id: int
    class Config:
        orm_mode = True
class Absence(CreateAndUpdateAbsence):
    id: int
    class Config:
        orm_mode = True


# TO support list and get APIs
class User(CreateAndUpdateUser):
    id: int
    class Config:
        orm_mode = True


# To support list users API
class PaginatedUserInfo(BaseModel):
    limit: int
    offset: int
    data: List[User]
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None
    role_id : int
class LoginInfo(BaseModel):
    email: Optional[str] = None
    pass_word : Optional[str] = None

