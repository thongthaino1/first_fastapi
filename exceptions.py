
from starlette.exceptions import HTTPException as StarletteHTTPException

class UserInfoException(Exception):
    ...


class UserInfoNotFoundError(UserInfoException):
    def __init__(self):
        self.status_code = 404
        self.detail = "User Info Not Found"


class UserInfoInfoAlreadyExistError(UserInfoException):
    def __init__(self):
        self.status_code = 409
        self.detail = "User Info Already Exists"
class AbsenceInfoException(Exception):
    ...


class AbsenceInfoNotFoundError(AbsenceInfoException):
    def __init__(self):
        self.status_code = 404
        self.detail = "Absence Info Not Found"


class AbsenceInfoInfoAlreadyExistError(AbsenceInfoException):
    def __init__(self):
        self.status_code = 409
        self.detail = "Absence Info Already Exists"


class WorkingException(Exception):
    ...


class WorkingNotFoundError(WorkingException):
    def __init__(self):
        self.status_code = 404
        self.detail = "Absence Info Not Found"


class WorkingInfoAlreadyExistError(WorkingException):
    def __init__(self):
        self.status_code = 409
        self.detail = "Working Info Already Exists"
class credentials_exception(StarletteHTTPException):
    def __init__(self):
        self.status_code = 401
        # self.detail = "Working Info Already Exists"
from fastapi import APIRouter, Depends, HTTPException,status
