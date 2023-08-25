from fastapi import APIRouter
from fastapi_utils.cbv import cbv
from sqlalchemy.orm import Session
# import crud_working
import exceptions, json
import schemas
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

import services.crud_absence
import services.working as wkService
from database import get_db
from services import crud
from exceptions import UserInfoException
from schemas import User
from typing import Annotated
from fastapi import Depends, HTTPException, status, Request
from datetime import datetime

router = APIRouter()
templates = Jinja2Templates(directory="templates")

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


# Example of Class based view
@cbv(router)
class Workings:
    session: Session = Depends(get_db)

    @router.get("/workings", response_class=HTMLResponse)
    def list_workings(
            self,
            request: Request,
            current_user: Annotated[str, Depends(crud.validate_token)],
            limit: int = 100, offset: int = 0,
    ):
        # if not current_user.role_id == 1 :
        # raise  credentials_exception
        # return  1
        event = data_name_id = []

        workings_list = wkService.get_all_workings_by_user_id(self.session, limit, offset, current_user.id)

        absences_list = services.crud_absence.get_all_absences_by_user_id(self.session, limit, offset, current_user.id)

        response = {"limit": limit, "offset": offset, "data": workings_list}
        user_id_list = crud.get_all_user_by_manager(self.session,current_user.id)
        for id in user_id_list:
            data_name_id.append({"id": id, "name": crud.get_user_info_by_id(self.session, id).name})


        for absen in absences_list:

            str_ab_date_start = datetime.strftime(absen.time_from, "%Y-%m-%d")
            str_ab_time_start = datetime.strftime(absen.time_from, "%H:%M")
            str_ab_date_end = datetime.strftime(absen.time_to, "%Y-%m-%d")
            str_ab_time_end = datetime.strftime(absen.time_to, "%H:%M")
            event.append(
                {"reason":"LY DO :"+absen.reason, "title": str_ab_time_start +"Nghi co phep" if absen.flag_allow else str_ab_time_start +"Nghi ko phep",
                 "start": str_ab_date_start, "end": str_ab_date_end, "backgroundColor": "pink" if absen.flag_allow else "black"})


        for work in response['data']:
                if work.checkinM:
                    work.checkin = work.checkinM
                else:
                    work.checkin = work.checkinA
                if work.checkoutM:
                    work.checkout = work.checkoutM
                else:
                    work.checkout = work.checkoutA
                for i in response['data']:
                    print(i.workingDate)
                str_wk_date = datetime.strftime(work.workingDate, "%Y-%m-%d")
                if work.checkin:
                    event.append({
                                  "title": "CHECK IN " + str(work.checkin.hour) + ":" + str(work.checkin.minute), "start": str_wk_date,
                                  "backgroundColor": 'red', 'allDay': 'true'})
                if work.checkout:
                    event.append(
                        { "title":  "CHECK OUT " + str(work.checkout.hour) + ":" + str(work.checkin.minute),
                         "start": str_wk_date, "backgroundColor": 'blue'})

        return templates.TemplateResponse("working.html", {"request": request, "response": response, "event": event,
                                                           "current_user": current_user, "data_name_id": data_name_id})

    # @router.get("/items/{id}"
    # async def read_item(request: Request, id: str):
    #     return templates.TemplateResponse("test.html", {"request": request, "id": id})

    # API endpoint to add a working info to the database
    @router.get("/workings/user/{user_id}")
    def list_workings_user(
            self, request: Request,
            current_user: Annotated[str, Depends(crud.validate_token)],
            user_id: int ,
            limit: int = 100, offset: int = 0,
    ):
        # return current_user
        if not current_user.role_id == 1 and not current_user.role_id == 2:
            raise credentials_exception
        user_id_list = crud.get_all_user_by_manager(self.session,current_user.id)
        # print(user_id_list,123123213)
        # return  user_id_list
        if user_id in user_id_list:
            event = data_name_id = []
            workings_list = wkService.get_all_workings_by_user_id(self.session, limit, offset, user_id)
            absences_list = services.crud_absence.get_all_absences_by_user_id(self.session, limit, offset, user_id)
            response = {"limit": limit, "offset": offset, "data": workings_list}
            for id in user_id_list :
                data_name_id.append({"id":id,"name":crud.get_user_info_by_id(self.session,id).name})

            for absen in absences_list :
                str_ab_date_start = datetime.strftime(absen.time_from, "%Y-%m-%d")
                str_ab_date_end = datetime.strftime(absen.time_to, "%Y-%m-%d")
                event.append(
                    {"id": str_ab_date_start, "title": "Nghi co phep" if absen.flag_allow else "Nghi ko phep",
                     "start": str_ab_date_start,"end":str_ab_date_end, "backgroundColor": 'pink'})
            for work in workings_list   :
                if work.checkinM:
                    work.checkin = work.checkinM
                else:
                    work.checkin = work.checkinA
                if work.checkoutM:
                    work.checkout = work.checkoutM
                else:
                    work.checkout = work.checkoutA
                # for i in response['data'] :
                #     print(i.workingDate)
                str_wk_date = datetime.strftime(work.workingDate, "%Y-%m-%d")
                if work.checkin:
                    event.append({"id": str_wk_date + " 1", "eventContent": 12242,
                                  "title": str(work.checkin.hour) + ":" + str(work.checkin.minute),
                                  "start": str_wk_date, "backgroundColor": 'red', 'allDay': 'true'})
                if work.checkout:
                    event.append(
                        {"id": str_wk_date + " 2", "title": str(work.checkout.hour) + ":" + str(work.checkin.minute),
                         "start": str_wk_date, "backgroundColor": 'blue'})


            return templates.TemplateResponse("working.html", {"request": request, "response": response, "event": event,
                                                               "current_user": current_user,"data_name_id":data_name_id})

        else:
            return "Khong dc phep "

    @router.post("/workings")
    def add_working(
            self,
            # working_info: schemas.CreateAndUpdateWorking,
            current_user: Annotated[str, Depends(crud.validate_token)]
    ):
        # return requests
        try:
            working_info = wkService.create_update_working(self.session, current_user.id)
            print(working_info.workingDate)
            return working_info
        except UserInfoException as cie:
            raise HTTPException(**cie.__dict__)


# API endpoint to get info of a particular working
@router.get("/user/workings")
def get_working_info_by_user(
        current_user: Annotated[User, Depends(crud.validate_token)],
        user_id: int,
        session: Session = Depends(get_db),
):
    if current_user.role_id == 1:
        try:
            working_info = crud_working.get_all_workings_by_user_id(session, current_user.id)
            return working_info
        except UserInfoException as cie:
            raise HTTPException(**cie.__dict__)
    else:
        raise credentials_exception


# @router.put("/workings/{working_id}")
# def update_working(working_id:int,new_info:CreateAndUpdateUser,session : Session = Depends(get_db)) :
#     try :
#         working_info = get_working_info_by_id(working_id)
#         return working_info
#     except UserInfoException as uie :
#         raise HTTPException(**cie.__dict__)


# API to update a existing working info
@router.put("/workings/{working_id}", response_model=schemas.Working)
def update_working(
        current_user: Annotated[User, Depends(crud.validate_token)],
        working_id: int,
        new_info: schemas.CreateAndUpdateWorking,
        session: Session = Depends(get_db),

):
    user_id = current_user.id
    if current_user.id == user_id or current_user.role_id == 1:
        try:
            working_info = crud_working.update_working_info(session, working_id, new_info, current_user.role_id)
            return working_info
        except exceptions.WorkingInfoNotFoundError as cie:
            raise HTTPException(**cie.__dict__)


# API to delete a working info from the data base
@router.delete("/workings/{working_id}")
def delete_working(
        current_user: Annotated[User, Depends(crud.validate_token)],
        working_id: int,
        session: Session = Depends(get_db)
):
    if current_user.role_id == 1:
        try:
            return wkService.delete_working_info(session, working_id)
        except UserInfoException as cie:
            raise HTTPException(**cie.__dict__)
    else:
        raise credentials_exception


@router.get("/login", response_class=HTMLResponse)
def login_Template(
        # current_user: Annotated[User, Depends(crud.validate_token)],
        request: Request
):
    # if "access_token" in request.cookies :
    #     user = crud.validate_token(request.cookies["access_token"])
    # if  isinstance(user,int) :
    #     print(user)
    #     return RedirectResponse(url="/check_in")
    # else:
    #     return templates.TemplateResponse("login.html", {"request": request})
    return templates.TemplateResponse("login.html", {"request": request})


@router.get("/logout", response_class=HTMLResponse)
def login_Template(
        # current_user: Annotated[User, Depends(crud.validate_token)],
        request: Request
):
    return templates.TemplateResponse("login.html", {"request": request})


@router.get("/check_in")
def test(
        current_user: Annotated[User, Depends(crud.validate_token)],
        request: Request
):
    return templates.TemplateResponse("test.html", {"request": request, "current_user": current_user})


@router.get("/test")
def test():
    student_score = {'Ritika': 5,
                     'Sam': 7,
                     'John': 10,
                     'Aadi': 8}
    # Print contents of dict in json like format

    print(json.dumps(student_score, indent=4))
    return 1
