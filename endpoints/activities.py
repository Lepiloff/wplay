from typing import List

from fastapi import APIRouter, Request, Form, Depends
from fastapi.templating import Jinja2Templates

from services.activities import ActivityService
from schemas.activity_schema import ActivityList, ActivityCreate

router = APIRouter()
templates = Jinja2Templates(directory="templates")


# TODO check fore what using smth like @router.post("/", response_class=HTMLResponse)

@router.get('/', response_model=List[ActivityList])
async def _activities(request: Request,
                      service: ActivityService = Depends()):
    result = await service.get()
    return templates.TemplateResponse('activity.html', context={'request': request, 'result': result})


@router.post('/', response_model=ActivityCreate)
async def activity_create(request: Request, name: str = Form(...),
                          service: ActivityService = Depends()):
    result = await service.post(name)
    return templates.TemplateResponse('activity.html', context={'request': request, 'result': result})

