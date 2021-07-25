import json
from fastapi import Request

from db import database
from broker.core.utils import consume_topic_message
from models.notifications import notifications
from services.auth import is_authenticated
from services.messages import MessagesService


async def add_user_data_to_request(request: Request, call_next, ):
    # TODO закинуть messages в редис , что бы не тащить их из базы ?
    response = await call_next(request)
    user = await is_authenticated(request)
    if user:
        # add user_id to response
        response.set_cookie(key="user_id", value=user)
        notifications = await MessagesService.get_count(user)
        if notifications:
            # add notification to response
            response.set_cookie(key="event_notifications", value=notifications['events']) \
                if notifications['events'] else None
            response.set_cookie(key="friend_notifications", value=notifications['friends']) \
                if notifications['friends'] else None
    return response
