from email.policy import default
from unittest.mock import DEFAULT

from multipart.multipart import NULL
from sqlalchemy import BigInteger
from sqlalchemy.schema import Column
from sqlalchemy.types import String, Integer,Float, Enum,DateTime,BigInteger,DATE,TIME
from database import Base
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum
from sqlalchemy import ForeignKey
from datetime import datetime


class UserInfo(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String,nullable=False)
    email = Column(String,nullable=False)
    phone = Column(String,default= "0705502529")
    role_id = Column(Integer,default= 2)
    pass_word = Column(String, nullable=False)
    email_verified_at = Column(DateTime(timezone=True), server_default=func.now())
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now() ,onupdate=func.now())
    rest_allowed_day = Column(Float,nullable=False,default = 12)

class Role(Base):
    __tablename__ = "roles"

    role_id = Column(Integer, primary_key=True, index=True)
    role = Column(String,nullable=False)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class Manager_User(Base):
    __tablename__ = "manager_user"

    id = Column(Integer, primary_key=True, index=True)
    manage_id = Column(Integer,nullable=False)
    user_id = Column(Integer,nullable=False)

class Absence(Base):
    __tablename__ = "absence"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer ,index=True)
    reason = Column(String)
    accepted = Column(Integer,default = 0)
    flag_allow = Column(Integer,default = 0)
    created_at = Column(DateTime(timezone=True), default=func.now())
    accepted_at = Column(DateTime(timezone=True))
    accept_id = Column(Integer,default = 0)
    time_from =  Column(DateTime(timezone=True))
    time_to = Column(DateTime(timezone=True))

class Add_WK(Base) :
    __tablename__ = "add_working"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    reason = Column(String)
    accepted = Column(Integer, default=0)
    flag_allow = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), default=func.now())
    accepted_at = Column(DateTime(timezone=True))
    accept_id = Column(Integer, default=0)
    time_from = Column(DateTime(timezone=True))
    time_to = Column(DateTime(timezone=True))
class Working(Base):
    __tablename__ = "working"


    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer ,index=True)
    workingDate = Column("workingDate",DateTime())
    checkinM = Column("checkinMorning",TIME(timezone=True))
    checkoutM = Column("checkoutMorning",TIME(timezone=True))
    checkinA = Column("checkinAfternoon",TIME(timezone=True))
    checkoutA = Column("checkoutAfternoon",TIME(timezone=True))
    workingTime = Column("workingTime",TIME(timezone=True))
