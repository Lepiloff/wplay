from fastapi import APIRouter, Request, Form, Depends
from fastapi.templating import Jinja2Templates

from services.activities import ActivityService


router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get('/')
async def main_page(request: Request,
                    activity_service: ActivityService = Depends()):
    activity = await activity_service.get()
    return templates.TemplateResponse('base.html', context={'request': request,
                                                            'activities': activity})
