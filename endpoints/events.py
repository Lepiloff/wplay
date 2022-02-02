from typing import List

from fastapi import APIRouter, Request, Form, Depends
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse
import starlette.status as status

from services.events import EventsService
from services.events_invites import InviteService
from services.auth import get_current_user
from schemas.event_schema import EventForm, EventBase, EventList, EventSingle
from helpers.map import Map


router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get('/all', response_model=List[EventList])
async def events_list(
        request: Request,
        service: EventsService = Depends(),
):
    events = await service.get_list()
    # TODO возможно из эндпоинта стоит вынести логику в сервис
    events_data = [
        (event['id'], event['title'], event['location']['lat'], event['location']['long'], event['activity']['name'])
        for event in events
    ]
    m = Map().show_events(events_data)
    return templates.TemplateResponse('events.html',
                                      context={
                                          'request': request,
                                          'events': events,
                                          'm': m._repr_html_(),
                                      }
                                      )


@router.post('/create', response_model=EventBase)
async def event_create(
        request: Request,
        user_id: str = Depends(get_current_user),
        service: EventsService = Depends(),
        form: EventForm = Depends(EventForm.as_form)
):
    # TODO event возвращает дикт хотя в запросе указано вернуть id
    event = await service.post(
        user_id,
        form.country,
        form.city,
        form.street,
        form.house,
        form.title,
        form.description,
        form.activity,
        form.is_private,
        form.start_date,
        form.start_time
   )
    redirect_url = request.url_for('get_event', **{'pk': event['id']})
    return RedirectResponse(redirect_url, status_code=status.HTTP_303_SEE_OTHER)


@router.get('/{pk}', response_model=EventSingle)
async def get_event(
        request: Request,
        pk: int,
        service: EventsService = Depends()
):
    event = await service.get(pk)
    # TODO возможно из эндпоинта стоит вынести логику в сервис
    tooltip = event['activity']['name']
    popup = event['title']
    event_coordinate = (event['location']['lat'], event['location']['long'])
    m = Map(event_coordinate, 15, popup, tooltip).show_event()
    #TODO dont show join button if user joined yet
    return templates.TemplateResponse(
        'event.html',
        context=
        {
            'request': request,
            'event': event,
            'm': m._repr_html_(),
        }
    )


#TODO response_model ?
@router.post('/{pk}/join')
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
    await service.request_to_join(pk, creator_id, from_user_id)
    # TODO success messages with data from invite result
    # TODO possible to get all data info from invite variable ?

    redirect_url = request.url_for('get_event', **{'pk': event['id']})
    return RedirectResponse(redirect_url, status_code=status.HTTP_303_SEE_OTHER)


@router.post('/invite/{pk}/decline')
async def decline_event_invite(
        request: Request,
        pk: int,
        user_id: str = Depends(get_current_user),
        service: InviteService = Depends(),
):
    await service.decline_invite(pk)
    redirect_url = request.url_for('user_profile', **{'pk': user_id})
    return RedirectResponse(redirect_url, status_code=status.HTTP_303_SEE_OTHER)


@router.post('/invite/{pk}/accept')
async def accept_event_invite(
        request: Request,
        pk: int,
        user_id: str = Depends(get_current_user),
        service: InviteService = Depends(),
):
    await service.accept_invite(pk)
    redirect_url = request.url_for('user_profile', **{'pk': user_id})
    return RedirectResponse(redirect_url, status_code=status.HTTP_303_SEE_OTHER)

