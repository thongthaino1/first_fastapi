from fastapi import APIRouter
from fastapi_utils.cbv import cbv
from sqlalchemy.orm import Session
import exceptions
import schemas, models
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from database import get_db
from services import crud, add_wk
from exceptions import UserInfoException
from schemas import User
from typing import Annotated

from fastapi import Depends, HTTPException, status, Request

router = APIRouter()
templates = Jinja2Templates(directory="templates")

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


# Example of Class based view
@cbv(router)
class add_wks:
    session: Session = Depends(get_db)

    @router.get("/add_wks", response_class=HTMLResponse)
    def list_add_wks(
            self, request: Request,
            current_user: Annotated[str, Depends(crud.validate_token)],
            limit: int = 20, offset: int = 0,

    ):
        # if not current_user.id == 1 :
        # raise  credentials_exception
        # print(current_user)
        user = crud.get_user_info_by_id(self.session, current_user.id)
        add_wks_list = add_wk.get_all_add_wks_by_user_id(self.session, limit, offset, current_user.id)
        response = {"limit": limit, "offset": offset, "data": add_wks_list}
        for i in add_wks_list:
            if crud.get_user_info_by_id(self.session, i.user_id):
                i.user_name = crud.get_user_info_by_id(self.session, i.user_id).name.title();

                accepter = crud.get_user_info_by_id(self.session, i.accept_id)

                if accepter:
                    i.accepter = crud.get_user_info_by_id(self.session, i.accept_id).name.title();
            else:
                i.user_name = " "
                i.accepter = " "

        return templates.TemplateResponse("add_wk.html", {"request": request, "response": response, "id": id,
                                                          "current_user": current_user,"user": user})

    @router.get("/add_wks_manage", response_class=HTMLResponse)
    def list_add_wks_manage(
            self, request: Request,
            current_user: Annotated[str, Depends(crud.validate_token)],
            limit: int = 20, offset: int = 0,

    ):
        # if not current_user.id == 1 :
        # raise  credentials_exception
        # print(current_user)
        add_wks_list = []
        if current_user.role_id == 1:
            add_wks_list = add_wk.get_all_add_wks_for_admin(self.session, limit, offset)
        elif current_user.role_id == 2:
            add_wks_list = add_wk.get_all_add_wks_by_manager_id(self.session, current_user.id, limit, offset)
        response = {"limit": limit, "offset": offset, "data_add_wks": add_wks_list}
        # print(add_wks_list)
        for i in add_wks_list:
            if crud.get_user_info_by_id(self.session, i.user_id):
                i.user_name = crud.get_user_info_by_id(self.session, i.user_id).name.title();

                accepter = crud.get_user_info_by_id(self.session, i.accept_id)

                if accepter:
                    i.accepter = crud.get_user_info_by_id(self.session, i.accept_id).name.title();
            else:
                i.user_name = " "
                i.accepter = " "

        return templates.TemplateResponse("manager_view.html", {"request": request, "response": response, "id": id,
                                                          "current_user": current_user})

    @router.get("/add_wks1")
    def list_add_wks121(
            self,
            current_user: Annotated[str, Depends(crud.validate_token)],
            limit: int = 10, offset: int = 0,

    ):

        add_wks_list = add_wk.get_all_add_wks(self.session, limit, offset)
        # print(add_wks_list)

        # add_wks_list = add_wk.get_add_wk_info_by_id(self.session,10)
        response = {"limit": limit, "offset": offset, "data": add_wks_list, "current_user": current_user}
        # return response

        return response

    # @router.get("/items/{id}"
    # async def read_item(request: Request, id: str):
    #     return templates.TemplateResponse("test.html", {"request": request, "id": id})

    # API endpoint to add a add_wk info to the database
    @router.post("/add_wks")
    def add_add_wk(
            self,
            add_wk_info: schemas.CreateAndUpdateAdd_WK,
            current_user: Annotated[User, Depends(crud.validate_token)]
    ):
        try:
            user_id = current_user.id
            add_wk_info = add_wk.create_add_wk(self.session, add_wk_info, user_id)
            # print(add_wk_info)
            return add_wk_info
        except UserInfoException as cie:
            raise HTTPException(**cie.__dict__)


@router.get("/add_wks_create", response_class=HTMLResponse)
def get_add_wk_html(
        request: Request,
        current_user: Annotated[str, Depends(crud.validate_token)],
        session: Session = Depends(get_db)

):
    user_id = current_user.id
    user = crud.get_user_info_by_id(session, user_id)
    # add_wk_info = add_wk.create_add_wk(session, user_id)
    # print(add_wk_info)
    # return add_wk_info
    return templates.TemplateResponse("create_add_wk.html",
                                      {"request": request, "user": user, "current_user": current_user})


# except UserInfoException as cie:
#     raise HTTPException(**cie.__dict__)


# API endpoint to get info of a particular add_wk
@router.get("/user/add_wks")
def get_add_wk_info_by_user(
        current_user: Annotated[User, Depends(crud.validate_token)],
        user_id: int,
        session: Session = Depends(get_db),
):
    if current_user.role_id == 1:
        try:
            add_wk_info = add_wk.get_all_add_wks_by_user_id(session, current_user.id)
            return add_wk_info
        except UserInfoException as cie:
            raise HTTPException(**cie.__dict__)
    else:
        raise credentials_exception


# @router.put("/add_wks/{add_wk_id}")
# def update_add_wk(add_wk_id:int,new_info:CreateAndUpdateUser,session : Session = Depends(get_db)) :
#     try :put
#         add_wk_info = get_add_wk_info_by_id(add_wk_id)
#         return add_wk_info
#     except UserInfoException as uie :
#         raise HTTPException(**cie.__dict__)


# API to update a existing add_wk info
@router.put("/add_wks/{add_wk_id}")
def update_add_wk(
        current_user: Annotated[User, Depends(crud.validate_token)],
        add_wk_id: int,
        new_info: schemas.CreateAndUpdateAdd_WK,
        session: Session = Depends(get_db),

):
    try:
        if current_user.role_id in (1, 2):
            add_wk_info = add_wk.update_add_wk_info(session, add_wk_id, current_user.id, new_info)
            return add_wk_info
    except exceptions.AbsenceInfoNotFoundError as cie:
        raise HTTPException(**cie.__dict__)

    return None


# API to delete a add_wk info from the data base
@router.delete("/add_wks/{add_wk_id}")
def delete_add_wk(
        current_user: Annotated[User, Depends(crud.validate_token)],
        add_wk_id: int,
        session: Session = Depends(get_db)
):
    if current_user.role_id == 1:
        try:
            return add_wk.delete_add_wk_info(session, add_wk_id)
        except UserInfoException as cie:
            raise HTTPException(**cie.__dict__)
    else:
        raise credentials_exception
