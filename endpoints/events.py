from typing import List

from fastapi import APIRouter, Depends, Request, Response
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse
import starlette.status as status

from models.users import users
from services.auth import get_current_user
from services.events import EventsService
from services.events_invites import InviteService
from services.user import UserService
from schemas.event_schema import EventForm, EventBase, EventList, EventSingle
from helpers.constants import EventNotification
from helpers.map import Map
from helpers.utils import CustomURLProcessor


router = APIRouter()
templates = Jinja2Templates(directory="templates")
templates.env.globals['CustomURLProcessor'] = CustomURLProcessor


@router.get('/all', response_model=List[EventList])
async def events_list(
        request: Request,
        service: EventsService = Depends(),
        user: users = Depends(UserService.get_authenticated_user_id),
):
    events = await service.get_list()
    events_data = [
        (
            event['id'], event['title'], event['location']['lat'],
            event['location']['long'], event['activity']['name']
        )
        for event in events
    ]
    m = await Map(zoom_start=12).show_events(events_data)
    return templates.TemplateResponse(
        'events.html',
        context={
            'request': request,
            'events': events,
            'm': m._repr_html_(),
            'user': user
        }
        )


@router.post('/create', response_model=EventBase)
async def event_create(
        request: Request,
        user: str = Depends(get_current_user),
        service: EventsService = Depends(),
        form: EventForm = Depends(EventForm.as_form)
):
    event_id = await service.post(
        user['user_id'],
        form.country,
        form.city,
        form.street,
        form.house,
        form.title,
        form.description,
        form.activity,
        form.members_count,
        form.is_private,
        form.start_date,
        form.start_time
    )
    redirect_url = request.url_for('get_event', **{'pk': event_id})
    return RedirectResponse(redirect_url, status_code=status.HTTP_303_SEE_OTHER)


@router.get('/{pk}', response_model=EventSingle)
async def get_event(
        request: Request,
        pk: int,
        service: EventsService = Depends(),
        invite_service: InviteService = Depends(),
        user: users = Depends(UserService.get_authenticated_user_id),
):
    event = await service.get(pk)
    tooltip = event['activity']['name']
    popup = event['title']
    event_coordinate = (event['location']['lat'], event['location']['long'])
    m = await Map(event_coordinate, 15, popup, tooltip).show_event()
    event_cancel_button, event_invite_button, show_processing_button = (
        await invite_service.is_show_event_invite_button(event, user)
    )
    return templates.TemplateResponse(
        'event.html',
        context={
            'request': request,
            'event': event,
            'm': m._repr_html_(),
            'user': user,
            'cancel_button': event_cancel_button,
            'invite_button': event_invite_button,
            'processing_button': show_processing_button
        }
    )


#TODO response_model ?
@router.post('/{pk}/join')
async def join_to_event(
        request: Request,
        pk: int,
        from_user: str = Depends(get_current_user),
        service: InviteService = Depends(),
        event_service: EventsService = Depends()
):
    event = await event_service.get(pk)
    creator_id = event['creator']
    result = await service.request_to_join(pk, creator_id, from_user['user_id'])
    redirect_url = request.url_for('get_event', **{'pk': event['id']})
    response = RedirectResponse(redirect_url, status_code=status.HTTP_303_SEE_OTHER)
    message = EventNotification.SUCCESS.value if result else EventNotification.NOT_SUCCESS.value
    response.set_cookie(
        'event_notifications',
        value=message,
        httponly=True,
        max_age=3,
        expires=3,
    )
    return response


@router.post('/invite/decline')
async def decline_event_invite(
        request: Request,
        event: int,
        event_invites: int,
        sender: int,
        message_id: int,
        user: str = Depends(get_current_user),
        service: InviteService = Depends(),
):
    await service.decline_invite(event, event_invites, sender, message_id, user['user_id'])
    redirect_url = request.url_for('user_notification', **{'pk': user['user_id']})
    return RedirectResponse(redirect_url, status_code=status.HTTP_303_SEE_OTHER)


@router.post('/invite/accept')
async def accept_event_invite(
        request: Request,
        event: int,
        event_invites: int,
        sender: int,
        message_id: int,
        user: str = Depends(get_current_user),
        service: InviteService = Depends(),
):
    await service.accept_invite(event, event_invites, sender, message_id, user['user_id'])
    redirect_url = request.url_for('user_notification', **{'pk': user['user_id']})
    return RedirectResponse(redirect_url, status_code=status.HTTP_303_SEE_OTHER)


@router.post('/cancel_participation')
async def cancel_participation(
        request: Request,
        event_id: int,
        event_owner: int,
        user: str = Depends(get_current_user),
        service: InviteService = Depends(),
):
    await service.decline_to_participate_in(event_id, event_owner, user['user_id'])
    redirect_url = request.url_for('get_event', **{'pk': event_id})
    return RedirectResponse(redirect_url, status_code=status.HTTP_303_SEE_OTHER)
