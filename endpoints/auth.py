import json

from fastapi import APIRouter, Depends, Request, Form, status
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordRequestForm
from starlette.responses import RedirectResponse

from services.auth import AuthService, get_current_user
from sessions.core.base import redis_cache

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get('/login')
async def sign_in(request: Request):
    return templates.TemplateResponse('login.html', context={'request': request})


@router.post('/login')
async def sign_in(
        user_data: OAuth2PasswordRequestForm = Depends(),
        service: AuthService = Depends(),
):
    session = await service.authenticate_user(
        user_data.username,
        user_data.password
    )
    response = RedirectResponse(url='/')
    response.set_cookie(
        'Authorization',
        value=session['session_id'],
        httponly=True,
        max_age=1800,
        expires=1800,
    )
    await redis_cache.set(session['session_id'], json.dumps(session['session_data']))
    return response


@router.post("/logout")
async def route_logout_and_remove_cookie():
    response = RedirectResponse(url="/")
    response.delete_cookie('Authorization')
    return response


@router.get('/current_user')
async def redis_keys():
    return await redis_cache.keys('*')


@router.get("/private")
def read_private(user_id: str = Depends(get_current_user)):
    return {"user_id": user_id}
