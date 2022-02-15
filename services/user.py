import itertools
import json

from sqlalchemy import select, desc, column, func, table, and_, text, join

from fastapi import HTTPException
from query import get_profile_info
from db import database
from models.events import events
from models.invites import event_invites
from models.messages import messages
from models.users import accounts


class UserService:

    async def get_user_info(self, pk: int):
        user = await database.fetch_one(query=get_profile_info, values={'pk': pk})
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        user = dict(user.items())
        return user

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
        ).select_from(event_invite).where(event_invites.c.to_user == pk).order_by(event_invites.c.created_at)
        events_invites = await database.fetch_all(query)
        return [dict(r.items()) for r in events_invites]


