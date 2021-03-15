from fastapi import APIRouter, Depends
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordRequestForm

from schemas.user_schema import UserCreate, Token


router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.post('/sign-up', response_model=Token)
async def sign_up(form_data: UserCreate):
    pass


@router.post('/sign-in', response_model=Token)
async def sign_in(form_data: OAuth2PasswordRequestForm = Depends()):
    pass
