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


@router.get("/download")
async def download_file():
    file_path = "static/img/6517.svg"
    return FileResponse(file_path, filename="my_file.svg", media_type="image/svg+xml")