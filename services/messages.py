from sqlalchemy import select
from starlette.responses import Response

from models.users import accounts
from models.messages import messages, NotificationType
from models.invites import event_invites
from models.events import events
from db import database
from query import get_message_count
from helpers.constants import Messages


class MessagesService:

    @staticmethod
    async def create(sender, recipient, event_id, event_invite, _type):
        query = messages.insert()
        values = {
            'recipient': recipient,
            'sender': sender,
            'event': event_id,
            'content': Messages.EVENT_INVITE.value,
            'event_invite': event_invite,
            'type': _type,
        }
        return await database.execute(query=query, values=values)

    @staticmethod
    async def get_count(user_id):
        result = await database.fetch_one(query=get_message_count, values={'user_id': user_id})
        return dict(result) if result else None

    @staticmethod
    async def get_messages(user_id):
        event_invite = messages.join(
            accounts, messages.c.sender == accounts.c.user_id).join(
            event_invites, messages.c.event_invite == event_invites.c.id
        ).join(events, messages.c.event == events.c.id)
        query = select(
            [
                messages.c.id, messages.c.sender, messages.c.event, messages.c.content,
                messages.c.created_at, messages.c.event_invite,
                event_invites.c.status, events.c.title, accounts.c.name, accounts.c.surname
            ]
        ).select_from(event_invite).where(messages.c.recipient == user_id).where(~messages.c.is_read)
        result = await database.fetch_all(query=query)
        return [dict(r.items()) for r in result] if result else None

    @staticmethod
    async def change_message_status(message_id: int):
        query = messages.update().where(messages.c.id == message_id)
        await database.execute(query=query, values={'is_read': True})

