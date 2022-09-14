from fastapi import Request

from services.auth import is_authenticated, get_current_user
from services.messages import MessagesService
from fastapi.responses import Response


async def get_user_notifications(request: Request, call_next):
    response = await call_next(request)
    if await is_authenticated(request):
        user = await get_current_user(request)
        if user['is_notified']:
            notifications = await MessagesService.get_count(user['user_id'])
            if notifications:
                # add notification to response
                response.set_cookie(
                    key="event_notifications",
                    value=notifications['events'],
                    httponly=True,
                ) if notifications['events'] else None
                response.set_cookie(
                    key="friend_notifications",
                    value=notifications['friends'],
                    httponly=True,
                ) if notifications['friends'] else None
    return response
