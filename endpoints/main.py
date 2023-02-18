from fastapi import APIRouter, Request, Form, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, FileResponse

from services.user import UserService
from models.users import users as User


router = APIRouter()
templates = Jinja2Templates(directory="templates")


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


@router.get('/test_static', response_class=FileResponse)
async def main_page(request: Request,
                    ):
    return FileResponse('base.html','static/img/6517.svg'
                                      )