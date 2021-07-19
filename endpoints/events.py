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
from starlette.responses import RedirectResponse


router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get('/', response_model=List[EventList])
async def events_list(
        request: Request,
        service: EventsService = Depends(),
        activity_service: ActivityService = Depends()
):
    ev = await service.get_list()
    activity = await activity_service.get()
    return templates.TemplateResponse('events.html', context={'request': request,
                                                              'activities': activity,
                                                              'result': ev})


@router.post('/', response_model=EventBase)
async def event_create(
        request: Request,
        user_id: str = Depends(get_current_user),
        service: EventsService = Depends(),
        form: EventForm = Depends(EventForm.as_form)
):
    event = await service.post(
        user_id,
        form.street,
        form.house,
        form.title,
        form.description,
        form.activity,
        form.is_private,
        form.start_date,
        form.start_time
   )
    return templates.TemplateResponse('event.html', context={'request': request, 'event': event})


@router.get('/{pk}', response_model=EventSingle)
async def event(
        request: Request,
        pk: int,
        service: EventsService = Depends()
):
    event = await service.get(pk)
    print (event)
    #TODO event отдает в юзере hashed_password , да и в принципе много лишней инфы, ебануть row sql напрашивается
    #TODO dont show join button if user joined yet
    return templates.TemplateResponse(
        'event.html',
        context=
        {
            'request': request,
            'event': event
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
    creator_id = event['creator']
    invite = await service.request_to_join(pk, creator_id, from_user_id)
    # TODO success messages with data from invite result
    # TODO possible to get all data info from invite variable ?
    if invite:
        data = {
            'invite': invite,
            'from_user_id': from_user_id,
            'to_user_id': creator_id,
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
