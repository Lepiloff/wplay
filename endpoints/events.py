from typing import List, Optional

from fastapi import APIRouter, Request, Form, Depends
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse
import starlette.status as status

from models.users import users as User
from services.auth import get_current_user
from services.events import EventsService
from services.events_invites import InviteService
from services.user import UserService
from schemas.event_schema import EventForm, EventBase, EventList, EventSingle
from helpers.map import Map
from helpers.utils import is_show_event_invite_button


router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get('/all', response_model=List[EventList])
async def events_list(
        request: Request,
        service: EventsService = Depends(),
        user: User = Depends(UserService.get_authenticated_user_id),
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
        user: User = Depends(UserService.get_authenticated_user_id),
):
    event = await service.get(pk)
    tooltip = event['activity']['name']
    popup = event['title']
    event_coordinate = (event['location']['lat'], event['location']['long'])
    m = await Map(event_coordinate, 15, popup, tooltip).show_event()
    #TODO отозвать заявку кнопка, метод decline_to_participate_in в InviteService
    event_invite_button = is_show_event_invite_button(event, user)
    templates = Jinja2Templates(directory="templates")
    return templates.TemplateResponse(
        'event.html',
        context={
            'request': request,
            'event': event,
            'm': m._repr_html_(),
            'user': user,
            'show_button': event_invite_button,
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
    await service.request_to_join(pk, creator_id, from_user['user_id'])
    # TODO success messages with data from invite result
    # TODO possible to get all data info from invite variable ?

    redirect_url = request.url_for('get_event', **{'pk': event['id']})
    return RedirectResponse(redirect_url, status_code=status.HTTP_303_SEE_OTHER)


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
    await service.decline_invite(event, event_invites, sender, message_id)
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
    await service.accept_invite(event, event_invites, sender, message_id)
    redirect_url = request.url_for('user_notification', **{'pk': user['user_id']})
    return RedirectResponse(redirect_url, status_code=status.HTTP_303_SEE_OTHER)

