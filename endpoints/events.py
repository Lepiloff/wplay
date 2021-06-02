import asyncio
import json


from typing import List

from fastapi import APIRouter, Request, Form, Depends
from fastapi.templating import Jinja2Templates

# from broker.invites.event_invite_producer import CallPikaConnector
from broker.core.utils import produce_topic_message
from services.events import EventsService
from services.events_invites import InviteService
from services.activities import ActivityService
from services.auth import get_current_user
from schemas.event_schema import EventForm, EventJoinForm, EventBase, EventList, EventSingle
from schemas.user_schema import User


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
    print (type(event))
    # data = {
    #     'title': event['title'],
    #     'creator': {k: v for x in event['creator'] for k, v in x.items()},
    #     'activity': {k: v for x in event['activity'] for k, v in x.items()},
    #     'users': event['users'],
    # }
    #TODO event отдает в юзере hashed_password , да и в принципе много лишней инфы, ебануть row sql напрашивается
    #TODO dont show join button if user joined yet
    return templates.TemplateResponse(
        'event.html',
        context=
        {
            'request': request,
            'event': event,
        }
    )


#TODO response_model ?
@router.post('/{pk}')
async def join_to_event(
        request: Request,
        pk: int,
        from_user_id: str = Depends(get_current_user),
        service: InviteService = Depends(),
        event_service: EventsService = Depends()
):
    #TODO  dont send invite to himself
    event = await event_service.get(pk)
    event_creator_id = event['creator'][0]['id']
    invite = await service.request_to_join(pk, event_creator_id, from_user_id)
    # TODO success messages with data from invite result
    # TODO possible to get all data info from invite variable ?
    if invite:
        data = {
            'invite': invite,
            'from_user_id': from_user_id,
            'to_user_id': event_creator_id,
            'message': 'You received join request to event: тест '
        }

        # Disable temporary
        # message = json.dumps(data).encode('utf8')
        # loop = asyncio.get_event_loop()
        # asyncio.ensure_future(produce_topic_message(loop, event_creator_id, message))

    return templates.TemplateResponse(
        'event_invite.html',
        context={
            'request': request,
            'result': event

        }
    )
