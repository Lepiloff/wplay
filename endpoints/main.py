from fastapi import APIRouter, Request, Form, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from services.user import UserService
from models.users import users as User
from helpers.utils import https_url_for


router = APIRouter()
templates = Jinja2Templates(directory="templates")
templates.env.globals['https_url_for'] = https_url_for


@router.get('/', response_class=HTMLResponse)
async def main_page(request: Request,
                    user: User = Depends(UserService.get_authenticated_user_id)
                    ):
    return templates.TemplateResponse('base.html',
                                      context={
                                          'request': request,
                                          'user': user,
                                      }
                                      )
