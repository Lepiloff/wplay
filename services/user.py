from sqlalchemy import select

from fastapi import HTTPException
from fastapi import Request
from helpers.utils import get_settings
from query import get_profile_info
from db import database
from models.events import events
from models.invites import event_invites
from models.messages import messages
from models.users import accounts, users
from sessions.core.base import redis_cache
from services.auth import is_authenticated, get_current_user


class UserService:

    async def get_user_info(self, pk: int):
        user = await database.fetch_one(query=get_profile_info, values={'pk': pk})
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return dict(user)

    @staticmethod
    async def get_user_events_invite_list(pk: int):
        event_invite = event_invites.join(
            accounts, event_invites.c.from_user == accounts.c.user_id).join(
            events, event_invites.c.to_event == events.c.id).join(
            messages, messages.c.event_invite == event_invites.c.id
        )
        query = select(
            [
             event_invites.c.id, event_invites.c.status, event_invites.c.from_user,
             event_invites.c.created_at, event_invites.c.to_event, events.c.title,
             accounts.c.name, accounts.c.surname, messages.c.id.label('message_id')
             ]
        ).select_from(event_invite).where(
            event_invites.c.to_user == pk
        ).order_by(
            event_invites.c.created_at
        )
        events_invites = await database.fetch_all(query)
        return [dict(r) for r in events_invites]

    @staticmethod
    async def change_user_notifications_status(user_id: str, value: bool):
        query = users.update().where(
            users.c.id == user_id
        ).values(is_notified=value)
        await database.fetch_one(query=query)
        # if user online also change redis user notifications data
        user_session = await redis_cache.hget(
            get_settings().user_session_id, user_id
        )
        if user_session:
            await redis_cache.hset(
                name=user_session,
                mapping={'is_notified': int(value)}
            )

    @staticmethod
    async def get_authenticated_user_id(request: Request):
        user = None
        if await is_authenticated(request):
            user = await get_current_user(request)
        return user
