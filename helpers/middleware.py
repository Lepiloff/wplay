from fastapi import Request, Response, status

from models.events import MembersQuantity
from services.activities import ActivityService
from services.auth import is_authenticated, get_current_user
from services.messages import MessagesService


async def get_user_notifications(request: Request, call_next):
    if await is_authenticated(request):
        user = await get_current_user(request)
        if user['is_notified']:
            notifications = await MessagesService.get_count(int(user['user_id']))
            if notifications:
                request.state.user_notifications = await MessagesService.get_count(int(user['user_id']))
    # https://stackoverflow.com/questions/71222144/runtimeerror-no-response-returned-in-fastapi-when-refresh-request
    try:
        response = await call_next(request)
    except RuntimeError as e:
        if await request.is_disconnected() and str(e) == "No response returned.":
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            raise
    return response


async def set_custom_attr(request: Request, call_next):
    """ Add custom data to request """
    request.state.activities = await ActivityService.get()
    request.state.members = [e.value for e in MembersQuantity]
    try:
        response = await call_next(request)
    except RuntimeError as e:
        if await request.is_disconnected() and str(e) == "No response returned.":
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            raise
    return response
