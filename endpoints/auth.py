from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordRequestForm
from starlette.responses import RedirectResponse

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
        "Authorization",
        value=session['session_id'],
        httponly=True,
        max_age=1800,
        expires=1800,
    )
    #TODO ограничить время жизни парамеров в редис
    sessions_data = await bool_to_int(session['session_data'])
    await redis_cache.hset(
        name=session['session_id'],
        mapping=sessions_data
    )
    # create table to match user_id and session_id
    #TODO ограничить время жизни парамеров в редис
    await redis_cache.hset(
        name=settings.user_session_id,
        mapping={sessions_data['user_id']: session['session_id']}
    )
    response.status_code = 302
    return response


# @router.get('/registrations')
# async def signup(request: Request):
#     return templates.TemplateResponse('sign_up.html', context={'request': request})


@router.post('/registrations')
async def signup(
        request: Request,
        service: AuthService = Depends(),
        form: UserCreateForm = Depends(UserCreateForm.as_form)
):
    #TODO есть register_new_user в AuthService
    print('Calling SignUP')
    print(form)
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


@router.get('/current_user')
async def redis_keys():
    print(await redis_cache.keys('*'))
    print(await redis_cache.hgetall('USER_SESSION_ID'))
    # print(await redis_cache.hget('USER_SESSION_ID'))
    # print(await redis_cache.hgetall('zw0aLWlgS4nT9grznj7JFDmM72hVvZtWUaadt8XxXhg='))
    return None
    # return await redis_cache.keys('*')

