from fastapi import APIRouter, Depends, Request, status, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordRequestForm
from starlette.responses import RedirectResponse
from sqlalchemy.sql.expression import select, update

from db import database
from config import Settings
from helpers.utils import bool_to_int, get_settings
from models.users import users as User
from schemas.user_schema import UserCreateForm
from services.auth import AuthService, get_current_user
from services.user import UserService
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
        settings: Settings = Depends(get_settings),
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
        max_age=3600,
        expires=3600,
    )
    sessions_data = await bool_to_int(session['session_data'])
    await redis_cache.hset(
        name=session['session_id'],
        mapping=sessions_data
    )
    # create table to match user_id and session_id
    #TODO так как нет возможности установить время жизни для вложенного ключа,
    # возможно надо сделать шедулед таск на очистку всех ключей в settings.user_session_id
    await redis_cache.hset(
        name=settings.user_session_id,
        mapping={sessions_data['user_id']: session['session_id']}
    )
    await redis_cache.expire(session['session_id'], 3600)
    response.status_code = 302
    return response


@router.post('/registration')
async def signup(
        request: Request,
        service: AuthService = Depends(),
        form: UserCreateForm = Depends(UserCreateForm.as_form)
):
    await service.register_new_user(request, form)
    return RedirectResponse(url='/', status_code=status.HTTP_303_SEE_OTHER)


@router.get("/logout")
async def logout(request: Request,
                 user: User = Depends(UserService.get_authenticated_user_id)):
    response = RedirectResponse(url="/", status_code=302)
    response.delete_cookie('Authorization')
    # clear notifications flag from request
    request.state._state.pop('user_notifications', None)
    # clear redis session data
    user_session = await redis_cache.hget(
        get_settings().user_session_id, str(user['user_id'])
    )
    if user_session:
        await redis_cache.delete(user_session)
    await redis_cache.hdel(get_settings().user_session_id, str(user['user_id']))
    return response


@router.get("/confirm_email")
async def confirm_email(token: str):
    # Check if the token exists in the database
    query = select([User.c.id, User.c.is_active]).where(User.c.email_verification_token == token)
    result = await database.fetch_one(query)
    if result is None:
        raise HTTPException(status_code=404, detail="Verification token not found")

    # Update the user's email confirmation status if the token is valid
    user_id, is_active = result
    print("is_active before update:", is_active)
    if is_active is not None and is_active:
        raise HTTPException(status_code=400, detail="Email address has already been confirmed")
    else:
        query = (
            update(User)
            .where(User.c.id == user_id)
            .values(is_active=True, email_verification_token=None)
        )
        await database.execute(query)
        return {"message": "Email confirmed successfully!"}


@router.get('/current_user')
async def redis_keys():
    print(await redis_cache.keys('*'))
    print(await redis_cache.hgetall('user_session_id'))
    # print(await redis_cache.hget('USER_SESSION_ID'))
    # print(await redis_cache.hgetall('zw0aLWlgS4nT9grznj7JFDmM72hVvZtWUaadt8XxXhg='))
    return None
    # return await redis_cache.keys('*')

