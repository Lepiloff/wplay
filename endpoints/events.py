from typing import List

from fastapi import APIRouter, Request, Form, Depends
from fastapi.templating import Jinja2Templates

from crud import events, activities
from schemas.activity_schema import ActivityList
from schemas.event_schema import EventForm, EventBase

router = APIRouter()
templates = Jinja2Templates(directory="templates")


# dont change method order
@router.get('/all')
async def _events():
    ev = await events.get_all()


@router.post('/', response_model=EventBase)
async def event_create(request: Request, form: EventForm = Depends(EventForm.as_form)):
    event = await events.post(form.street, form.house, form.title, form.content, form.activity)
    return templates.TemplateResponse('event.html', context={'request': request, 'result': event})


@router.get('/', response_model=List[ActivityList])
async def event_create(request: Request):
    activity = await activities.get()
    return templates.TemplateResponse('events.html', context={'request': request, 'result': activity})


@router.get('/{pk}')
async def event(request: Request, pk: int):
    event = await events.get(pk)
    # return templates.TemplateResponse('events.html', context={'request': request, 'result': event})
