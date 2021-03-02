from typing import List

from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates

from crud import activities
from schemas.activity_schema import ActivityList, ActivityCreate

router = APIRouter()
templates = Jinja2Templates(directory="templates")


# TODO check fore what using smth like @router.post("/", response_class=HTMLResponse)

@router.get('/', response_model=List[ActivityList])
async def _activities(request: Request):
    result = await activities.get()
    return templates.TemplateResponse('activity.html', context={'request': request, 'result': result})


@router.post('/', response_model=ActivityCreate)
async def activity_create(request: Request, name: str = Form(...)):
    result = await activities.post(name)
    return templates.TemplateResponse('activity.html', context={'request': request, 'result': name})

