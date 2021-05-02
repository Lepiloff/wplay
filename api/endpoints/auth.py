from fastapi import APIRouter, Depends, Request, Form, status
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordRequestForm

from schemas.user_schema import UserCreate, Token, User
from api.services.auth import AuthService, get_current_user


router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.post('/sign-up', response_model=Token, status_code=status.HTTP_201_CREATED,)
async def sign_up(
        user_data: UserCreate,
        service: AuthService = Depends()
):
    return await service.register_new_user(user_data)


@router.post('/sign-in', response_model=Token)
async def sign_in(
        user_data: OAuth2PasswordRequestForm = Depends(),
        service: AuthService = Depends(),
):
    return await service.authenticate_user(
        user_data.username,
        user_data.password
    )


@router.get('/user', response_model=User)
async def get_user(user: User = Depends(get_current_user)):
    return user




