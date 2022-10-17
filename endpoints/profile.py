from fastapi import APIRouter, Request, Response, Form, Depends
from fastapi import HTTPException, status
from fastapi.templating import Jinja2Templates

from services.messages import MessagesService
from services.user import UserService
from models.invites import InviteStatus
from models.users import users as User
from helpers.utils import CustomURLProcessor


router = APIRouter()
templates = Jinja2Templates(directory="templates")
templates.env.globals['CustomURLProcessor'] = CustomURLProcessor


@router.get('/{pk}')
async def user_profile(
        request: Request,
        pk: int,
        service: UserService = Depends(),
        user: User = Depends(UserService.get_authenticated_user_id)
):
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
        service: MessagesService = Depends(),
        user: User = Depends(UserService.get_authenticated_user_id)
):
    messages = await service.get_messages(pk)
    messages = messages if messages else {}
    # clear new notification flag
    await UserService.change_user_notifications_status(pk, False)
    response = templates.TemplateResponse(
        'notifications.html',
        context=
        {
            'request': request,
            'messages': messages,
            'invite_status': InviteStatus,
            'user': user,
        }
    )
    # clear notifications flag from request
    request.state._state.pop('user_notifications', None)
    # hide message with recalled status after first demonstration
    recalled_messages = [
        d['id'] for d in messages
        if 'id' in d and d['status'] == InviteStatus.RECALLED
    ]
    #TODO update in bulk
    if recalled_messages:
        await MessagesService.change_message_status(recalled_messages[0])
    return response
