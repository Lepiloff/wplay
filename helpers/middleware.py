from fastapi import Request

from services.auth import is_authenticated
from services.messages import MessagesService


async def add_user_data_to_request(request: Request, call_next, ):
    # TODO закинуть messages в редис , что бы не тащить их из базы ?
    response = await call_next(request)
    user = await is_authenticated(request)
    if user:
        # add user_id to response
        response.set_cookie(
            key="user_id",
            value=user,
            httponly=True,
            max_age=1800,
            expires=60,
        )
        notifications = await MessagesService.get_count(user)
        print(f'Notifications: {notifications}')
        if notifications:
            # add notification to response
            response.set_cookie(
                key="event_notifications",
                value=notifications['events'],
                httponly=True,
                max_age=1800,
                expires=1800,
            ) if notifications['events'] else None
            response.set_cookie(
                key="friend_notifications",
                value=notifications['friends'],
                httponly=True,
                max_age=1800,
                expires=1800,
            ) if notifications['friends'] else None
    return response
