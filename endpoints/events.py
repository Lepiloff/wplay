from typing import List

from fastapi import APIRouter, Request, Form, Depends
from fastapi.templating import Jinja2Templates

from crud.events import EventsService
from crud.activities import ActivityService
from schemas.activity_schema import ActivityList
from schemas.event_schema import EventForm, EventBase, EventList

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get('/', response_model=List[EventList])
async def all_events(request: Request,
                     service: EventsService = Depends(),
                     activity_service: ActivityService = Depends()):
    ev = await service.get_list()
    activity = await activity_service.get()
    return templates.TemplateResponse('events.html', context={'request': request,
                                                              'activities': activity,
                                                              'result': ev})


@router.post('/', response_model=EventBase)
async def event_create(request: Request,
                       service: EventsService = Depends(),
                       form: EventForm = Depends(EventForm.as_form)):
    event = await service.post(form.street, form.house, form.title, form.content, form.activity)
    return templates.TemplateResponse('event.html', context={'request': request, 'result': event})


@router.get('/{pk}')
async def event(request: Request, pk: int, service: EventsService = Depends()):
    event = await service.get(pk)
    # return templates.TemplateResponse('events.html', context={'request': request, 'result': event})
