from fastapi import APIRouter, Request, Form, Depends
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get('/')
async def main_page(request: Request):
    return templates.TemplateResponse('base.html', context={'request': request})
