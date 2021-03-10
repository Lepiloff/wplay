from typing import List

from fastapi import APIRouter, Request, Form, Depends
from fastapi.templating import Jinja2Templates

from crud import events, activities
from schemas.activity_schema import ActivityList
from schemas.event_schema import EventForm, EventBase, EventList

router = APIRouter()
templates = Jinja2Templates(directory="templates")


# dont change method order
@router.get('/', response_model=List[EventList])
async def all_events(request: Request):
    ev = await events.get_all()
    return templates.TemplateResponse('events.html', context={'request': request, 'result': ev})


@router.post('/create', response_model=EventBase)
async def event_create(request: Request, form: EventForm = Depends(EventForm.as_form)):
    event = await events.post(form.street, form.house, form.title, form.content, form.activity)
    return templates.TemplateResponse('event.html', context={'request': request, 'result': event})


@router.get('/{pk}')
async def event(request: Request, pk: int):
    event = await events.get(pk)
    # return templates.TemplateResponse('events.html', context={'request': request, 'result': event})
