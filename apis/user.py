from fastapi import APIRouter
from fastapi_utils.cbv import cbv
from sqlalchemy.orm import Session
from urllib3 import HTTPResponse
from fastapi.responses import HTMLResponse

from services.crud import validate_token, get_all_users, create_user, get_user_info_by_id, update_user_info, delete_user_info, \
    authenticate_user, create_access_token

from database import get_db
from exceptions import UserInfoException
from schemas import User, LoginInfo, CreateAndUpdateUser, PaginatedUserInfo
from datetime import timedelta

from fastapi import APIRouter
from fastapi_utils.cbv import cbv
from sqlalchemy.orm import Session
import exceptions
import schemas, models
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from database import get_db
from services import crud, crud_absence
from exceptions import UserInfoException
from schemas import User
from typing import Annotated

from fastapi import Depends, HTTPException, status, Request

router = APIRouter()
credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)
templates = Jinja2Templates(directory="templates")


# Example of Class based view
@cbv(router)
class Users:
    session: Session = Depends(get_db)
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    # user  = Annotated[User,Depends(validate_token)]
    # API to get the list of user info
    # @router.get("/users", response_model=PaginatedUserInfo, dependencies=Depends(validate_token))
    templates = Jinja2Templates(directory="templates")

    @router.get("/users", response_class=HTMLResponse)
    # @router.get("/users")
    def list_users(
            self,
            current_user : Annotated[str,Depends(validate_token)],
            request : Request,
            limit: int = 10,
            offset: int = 0,
                   ):
        # return  current_user
        # print(current_user)
        # if not current_user.role_id != 1 :
        #     raise  self.credentials_exception
        users_list = get_all_users(self.session, limit, offset)
        response = {"limit": limit, "offset": offset, "data": users_list}
        return templates.TemplateResponse("user.html", {"request": request, "response": response,"current_user":current_user})

        return response
    # def read_own_items(
    #         current_user: Annotated[User, Depends(validate_token)]
    # ):
    #     return [{"item_id": "Foo", "owner": current_user.username}]
        # print(oauth2_scheme(request=1))
        # return 1

    # API endpoint to add a user info to the database
    @router.post("/users")
    def add_user(
            self, user_info: CreateAndUpdateUser,
        # current_user: Annotated[str, Depends(validate_token)]
                 ):
        try:
            user_info = create_user(self.session, user_info)
            return user_info

        except UserInfoException as cie:
            raise HTTPException(**cie.__dict__)


# API endpoint to get info of a particular user
@router.get("/users/{user_id}", response_model=User)
def get_user_info(current_user: Annotated[User, Depends(validate_token)] ,
                  user_id: int, session: Session = Depends(get_db),
                  ):
    #decode token
    #
    if current_user.id == user_id or current_user.role_id == 1 :
        try:
            user_info = get_user_info_by_id(session, user_id)
            return user_info
        except UserInfoException as cie:
            raise HTTPException(**cie.__dict__)
    else :
        raise credentials_exception


# @router.put("/users/{user_id}")
# def update_user(user_id:int,new_info:CreateAndUpdateUser,session : Session = Depends(get_db)) :
#     try :
#         user_info = get_user_info_by_id(user_id)
#         return user_info
#     except UserInfoException as uie :
#         raise HTTPException(**cie.__dict__)


# API to update a existing user info
@router.put("/users/{user_id}", response_model=User)
def update_user(user_id: int, new_info: CreateAndUpdateUser, session: Session = Depends(get_db)):
    try:
        user_info = update_user_info(session, user_id, new_info)
        return user_info
    except UserInfoException as cie:
        raise HTTPException(**cie.__dict__)


# API to delete a user info from the data base
@router.delete("/users/{user_id}")
def delete_user(user_id: int, session: Session = Depends(get_db)):
    try:
        return delete_user_info(session, user_id)
    except UserInfoException as cie:
        raise HTTPException(**cie.__dict__)


@router.post("/token")
def login_for_access_token(
        requests : Request,
        form_data: LoginInfo,
        session: Session = Depends(get_db),

):
    # return requests._json
    user = authenticate_user(session, form_data.email, form_data.pass_word)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=2000000)
    access_token = create_access_token(
        data={"sub": user.email, "role_id": user.role_id,"secret":"0706600425","name":user.name}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
