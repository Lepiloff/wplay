from typing import List

from fastapi import APIRouter, Request, Form, Depends
from fastapi.templating import Jinja2Templates

from services.events import EventsService
from services.events_invites import InviteService
from services.activities import ActivityService
from schemas.event_schema import EventForm, EventInviteForm, EventBase, EventList, EventSingle

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get('/', response_model=List[EventList])
async def all_events(
        request: Request,
        service: EventsService = Depends(),
        activity_service: ActivityService = Depends()
):
    ev = await service.get_list()
    print(ev)
    activity = await activity_service.get()
    return templates.TemplateResponse('events.html', context={'request': request,
                                                              'activities': activity,
                                                              'result': ev})


@router.post('/', response_model=EventBase)
async def event_create(
        request: Request,
        service: EventsService = Depends(),
        form: EventForm = Depends(EventForm.as_form)
):
    event = await service.post(form.street, form.house, form.title, form.content, form.activity)
    return templates.TemplateResponse('event.html', context={'request': request, 'result': event})


@router.get('/{pk}', response_model=EventSingle)
async def event(
        request: Request,
        pk: int,
        service: EventsService = Depends()
):
    event = await service.get(pk)
    print (event)
    print (type(event['creator'][0]['id']))
    #TODO event отдает в юзере hashed_password , нужен ли он
    return templates.TemplateResponse(
        'event_invite.html',
        context=
        {
            'request': request,
            'result': event,
            'to_user': event['creator'][0]['id']
        }
    )


#TODO response_model ?
@router.post('/{pk}')
async def event_invite(
        request: Request,
        pk: int,
        form: EventInviteForm = Depends(EventInviteForm.as_form),
        service: InviteService = Depends()
):
    #TODO get_current_user ,  dont send invite to himself
    from_user_id = 1
    invite = await service.invite_send(pk, form.to_user_id, from_user_id)
    # TODO success messages
    return templates.TemplateResponse(
        'event_invite.html',
        context={
            'request': request,
            'result': invite

        }
    )
