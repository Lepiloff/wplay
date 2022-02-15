from fastapi import APIRouter, Request, Form, Depends
from fastapi import HTTPException, status
from fastapi.templating import Jinja2Templates

from services.messages import MessagesService
from services.user import UserService
from models.invites import InviteStatus
from helpers.utils import CustomURLProcessor


router = APIRouter()
templates = Jinja2Templates(directory="templates")
templates.env.globals['CustomURLProcessor'] = CustomURLProcessor


@router.get('/{pk}')
async def user_profile(
        request: Request,
        pk: int,
        service: UserService = Depends()
):
    user = await service.get_user_info(pk)
    events_invites = await service.get_user_events_invite_list(pk)
    return templates.TemplateResponse(
        'profile.html',
        context=
        {
            'request': request,
            'user': user,
            'events_invites': events_invites,
            'invite_status': InviteStatus,
        }
    )


@router.get('/{pk}/notifications')
async def user_notification(
        request: Request,
        pk: int,
        service: MessagesService = Depends()
):
    messages = await service.get_messages(pk)
    messages = messages if messages else {}
    return templates.TemplateResponse(
        'notifications.html',
        context=
        {
            'request': request,
            'messages': messages,
            'invite_status': InviteStatus,
        }
    )
