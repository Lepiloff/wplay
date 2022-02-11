import json

from fastapi import APIRouter, Depends, Request, Form, status
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordRequestForm
from starlette.responses import RedirectResponse

from services.auth import AuthService, get_current_user
from sessions.core.base import redis_cache

router = APIRouter()
templates = Jinja2Templates(directory="templates")


# @router.get('/login')
# async def login(request: Request):
#     return templates.TemplateResponse('sign_in.html', context={'request': request})


@router.post('/login')
async def login(
        user_data: OAuth2PasswordRequestForm = Depends(),
        service: AuthService = Depends(),
):
    session = await service.authenticate_user(
        user_data.username,
        user_data.password
    )
    response = RedirectResponse(url='/')
    response.set_cookie(
        "Authorization",
        value=session['session_id'],
        httponly=True,
        max_age=1800,
        expires=1800,
    )
    await redis_cache.set(session['session_id'], json.dumps(session['session_data']), ex=1800)
    response.status_code = 302
    return response


# @router.get('/registrations')
# async def signup(request: Request):
#     return templates.TemplateResponse('sign_up.html', context={'request': request})


@router.post('/registrations')
async def signup(
        user_data: OAuth2PasswordRequestForm = Depends(),
        service: AuthService = Depends(),
):
    pass
    # session = await service.authenticate_user(
    #     user_data.username,
    #     user_data.password
    # )
    # response = RedirectResponse(url='/')
    # response.set_cookie(
    #     "Authorization",
    #     value=session['session_id'],
    #     httponly=True,
    #     max_age=1800,
    #     expires=1800,
    # )
    # #TODO set expired time equal response cookie
    # await redis_cache.set(session['session_id'], json.dumps(session['session_data']))
    # return response


@router.get("/logout")
async def logout():
    response = RedirectResponse(url="/", status_code=302)
    response.delete_cookie('Authorization')
    response.delete_cookie('user_id')
    response.delete_cookie('event_notifications')
    return response


@router.get('/current_user')
async def redis_keys():
    return await redis_cache.keys('*')


@router.get("/private")
def read_private(request: Request, user_id: str = Depends(get_current_user)):
    # print (request.cookies.get("Incoming"))
    return {"user_id": user_id}
