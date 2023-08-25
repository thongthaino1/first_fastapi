# main.py
# Import FastAPI
import apis
from apis import user  as api_user
from apis import absence  as api_absence
from apis import working  as api_working
from apis import add_wk  as api_add_wk

from fastapi.responses import RedirectResponse
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.requests import Request

app = FastAPI()

app.include_router(api_absence.router)
app.include_router(api_user.router)
app.include_router(api_working.router)
app.include_router(api_add_wk.router)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
# credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials,please come to Login page",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
# request : Request
# request.headers.get("Authorization") = 1
# GET operation at route '/'
# @app.middleware("http")
# async def add_process_time_header(request: Request, call_next):
#     # request.headers["Authorization"] = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6" \
#     #                                     "IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsInJvbGVfaWQiO" \
#     #                                     "jEsInNlY3JldCI6IjA3MDY2MDA0MjUiLCJle" \
#     #                                     "HAiOjE4MTAzNjM0NDF9.fSq9lhk5yrXfZXWWUQq2N3KWwF6LSOza2HbvZde7ATc"
#     start_time = time.time()
#     response = await call_next(request)
#     process_time = time.time() - start_time
#     response.headers["Authorization"] = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6" \
#                                         "IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsInJvbGVfaWQiO" \
#                                         "jEsInNlY3JldCI6IjA3MDY2MDA0MjUiLCJle" \
#                                         "HAiOjE4MTAzNjM0NDF9.fSq9lhk5yrXfZXWWUQq2N3KWwF6LSOza2HbvZde7ATc"
#     print(response)
#     return response
@app.middleware("http")
async def create_auth_header(
    request: Request,
    call_next
):
    """
    Check if there are cookies set for authorization. If so, construct the
    Authorization header and modify the request (unless the header already
    exists!)
    """

    if (
        "Authorization" not in request.headers
        and "access_token" in request.cookies
        # and "access_token_signature" in request.cookies
    ):
        access_token = request.cookies["access_token"]
        # access_token_signature = request.cookies["access_token_signature"]
        # access_token = f"{access_token_payload}.{access_token_signature}"
        request.headers.__dict__["_list"].append(
            (
                "authorization".encode(),
                f"Bearer {access_token}".encode()
            )
        )
    response = await call_next(request)
    # else :
    #     response = RedirectResponse(url='/login')
    return response

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    # print(123)
    print(exc.__dict__)
    # if exc.status_code == 401:
    #     print("UNAUTH")
    return RedirectResponse(url='/login')
@app.get('/')
def root_api(request : Request):
    print(request.headers["authorization"] if "authorization" in  request.headers else None)
    return {"message": "Welcome to Balasundar's Technical Blog"}
    # return  RedirectResponse(url='/login')

# @app.get("/items/{id}", response_class=HTMLResponse)
@app.get("/items/{id}", response_class=HTMLResponse)
async def read_item(request: Request, id: str):
    return templates.TemplateResponse("test.html", {"request": request, "id": id})
