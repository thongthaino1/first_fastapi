from time import strftime

from fastapi import APIRouter
from fastapi_utils.cbv import cbv
from sqlalchemy.orm import Session
import exceptions
import schemas, models
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from database import get_db
from services import crud, crud_absence,add_wk
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
class Absences:
    session: Session = Depends(get_db)

    @router.get("/absences", response_class=HTMLResponse)
    def list_absences(
            self, request: Request,
            current_user: Annotated[str, Depends(crud.validate_token)],
            limit: int = 20, offset: int = 0,

    ):
        # if not current_user.id == 1 :
        # raise  credentials_exception
        # print(current_user)
        absences_list = []
        user = crud.get_user_info_by_id(self.session, current_user.id)
        absences_list = crud_absence.get_all_absences_by_user_id(self.session,limit, offset, current_user.id)
        add_wks_list = add_wk.get_all_add_wks_by_user_id(self.session, limit, offset, current_user.id)

        print(current_user.id,absences_list)
        response = {"limit": limit, "offset": offset, "data_absence": absences_list,"data_add_wk": add_wks_list}
        for i in (absences_list+add_wks_list):

            if i.user_id and crud.get_user_info_by_id(self.session, i.user_id)  :
                i.user_name = crud.get_user_info_by_id(self.session, i.user_id).name.title();

                accepter = crud.get_user_info_by_id(self.session, i.accept_id)

                if accepter :
                    i.accepter = crud.get_user_info_by_id(self.session, i.accept_id).name.title();
            else:
                i.user_name = " "
                i.accepter = " "

        return templates.TemplateResponse("absence.html", {"request": request, "response": response, "id": id,
                                                           "current_user":current_user,"user":user})

    @router.get("/absences_manage", response_class=HTMLResponse)
    def list_absences_by_manager(
            self, request: Request,
            current_user: Annotated[str, Depends(crud.validate_token)],
            limit: int = 20, offset: int = 0,

    ):
        # if not current_user.id == 1 :
        # raise  credentials_exception
        # print(current_user)
        if current_user.role_id == 1:
            absences_list = crud_absence.get_all_absences_for_admin(self.session, limit, offset)
            add_wks_list = add_wk.get_all_add_wks_for_admin(self.session, limit, offset)
        elif current_user.role_id == 2:
            absences_list = crud_absence.get_all_absences_by_manager_id(self.session, current_user.id, limit, offset)
            add_wks_list = add_wk.get_all_add_wks_by_manager_id(self.session, current_user.id, limit, offset)

        # print(current_user.id, absences_list)
        response = {"limit": limit, "offset": offset, "data_absence": absences_list,"data_add_wk": add_wks_list}
        for i in absences_list:
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

    @router.get("/absences1")
    def list_absences121(
            self,
            current_user: Annotated[str, Depends(crud.validate_token)],
            limit: int = 10, offset: int = 0,

    ):

        absences_list = crud_absence.get_all_absences(self.session, limit, offset)
        # print(absences_list)

        # absences_list = crud_absence.get_absence_info_by_id(self.session,10)
        response = {"limit": limit, "offset": offset, "data": absences_list,"current_user":current_user}
        # return response

        return response

    # @router.get("/items/{id}"
    # async def read_item(request: Request, id: str):
    #     return templates.TemplateResponse("test.html", {"request": request, "id": id})

    # API endpoint to add a absence info to the database
    @router.post("/absences")
    def add_absence(
            self,
            absence_info: schemas.CreateAndUpdateAbsence,
            current_user: Annotated[User, Depends(crud.validate_token)]
    ):
        try:
            user_id = current_user.id
            absence_info = crud_absence.create_absence(self.session, absence_info, user_id)
            # print(absence_info)
            return absence_info
        except UserInfoException as cie:
            raise HTTPException(**cie.__dict__)


@router.get("/absences_create", response_class=HTMLResponse)
def get_absence_html(
        request: Request,
        current_user: Annotated[str, Depends(crud.validate_token)],
        session: Session = Depends(get_db)

):
    user_id = current_user.id
    user = crud.get_user_info_by_id(session, user_id)
    # absence_info = crud_absence.create_absence(session, user_id)
    # print(absence_info)
    # return absence_info
    return templates.TemplateResponse("create_absence.html", {"request": request, "user": user,"current_user":current_user})


# except UserInfoException as cie:
#     raise HTTPException(**cie.__dict__)


# API endpoint to get info of a particular absence
@router.get("/user/absences")
def get_absence_info_by_user(
        current_user: Annotated[User, Depends(crud.validate_token)],
        user_id: int,
        session: Session = Depends(get_db),
):
    if current_user.role_id == 1:
        try:
            absence_info = crud_absence.get_all_absences_by_user_id(session, current_user.id)
            return absence_info
        except UserInfoException as cie:
            raise HTTPException(**cie.__dict__)
    else:
        raise credentials_exception


# @router.put("/absences/{absence_id}")
# def update_absence(absence_id:int,new_info:CreateAndUpdateUser,session : Session = Depends(get_db)) :
#     try :
#         absence_info = get_absence_info_by_id(absence_id)
#         return absence_info
#     except UserInfoException as uie :
#         raise HTTPException(**cie.__dict__)


# API to update a existing absence info
@router.put("/absences/{absence_id}")
def update_absence(
        current_user: Annotated[User, Depends(crud.validate_token)],
        absence_id: int,
        new_info: schemas.CreateAndUpdateAbsence,
        session: Session = Depends(get_db),

):
    try:
        if current_user.role_id in (1,2):
            absence_info = crud_absence.update_absence_info(session, absence_id, current_user.id, new_info)
            return absence_info
    except exceptions.AbsenceInfoNotFoundError as cie:
        raise HTTPException(**cie.__dict__)

    return None


# API to delete a absence info from the data base
@router.delete("/absences/{absence_id}")
def delete_absence(
        current_user: Annotated[User, Depends(crud.validate_token)],
        absence_id: int,
        session: Session = Depends(get_db)
):
    if current_user.role_id == 1:
        try:
            return crud_absence.delete_absence_info(session, absence_id)
        except UserInfoException as cie:
            raise HTTPException(**cie.__dict__)
    else:
        raise credentials_exception
