from fastapi import APIRouter, Request, Form, Depends
from fastapi.templating import Jinja2Templates

from services.user import UserService
from models.invites import InviteStatus

router = APIRouter()
templates = Jinja2Templates(directory="templates")


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
