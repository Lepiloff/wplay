from typing import List

from fastapi import APIRouter, Request, Form, Depends
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse

from services.events import EventsService
from services.events_invites import InviteService
from services.activities import ActivityService
from services.auth import get_current_user
from schemas.event_schema import EventForm, EventBase, EventList, EventSingle


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

    message = 'Invite sending successfully' if invite else 'Invite was not send'
    status = False if not invite else True

    return templates.TemplateResponse(
        'event.html',
        context={
            'request': request,
            'event': event,
            'message': message,
            'status': status
        }
    )


@router.get('/invite/{pk}/decline')
async def decline_event_invite(
        request: Request,
        pk: int,
        user_id: str = Depends(get_current_user),
        service: InviteService = Depends(),
):
    await service.decline_invite(pk)
    redirect_url = request.url_for('user_profile', **{'pk': user_id})
    return RedirectResponse(redirect_url)


@router.get('/invite/{pk}/accept')
async def accept_event_invite(
        request: Request,
        pk: int,
        user_id: str = Depends(get_current_user),
        service: InviteService = Depends(),
):
    await service.accept_invite(pk)
    redirect_url = request.url_for('user_profile', **{'pk': user_id})
    return RedirectResponse(redirect_url)

