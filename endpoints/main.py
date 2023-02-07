from typing import Any
from fastapi import APIRouter, Request, Form, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from services.user import UserService
from models.users import users as User



def https_url_for(request: Request, name: str, **path_params: Any) -> str:

    http_url = request.url_for(name, **path_params)

    # Replace 'http' with 'https'
    return http_url.replace("http", "https", 1)

router = APIRouter()
templates = Jinja2Templates(directory="templates")
templates.env.globals["https_url_for"] = https_url_for


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
