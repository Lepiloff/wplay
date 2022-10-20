from typing import Optional

from sqlalchemy.sql.expression import select

from db import database
from models.invites import event_invites, InviteStatus
from models.events import event_users
from services.messages import MessagesService
from services.user import UserService
from helpers.constants import Messages

EVENT = 'EVENT'


# TODO добавить функционал приглашения пользователя в ивент


class InviteService:

    @staticmethod
    async def get(
            pk: Optional[int] = None,
            user_id: Optional[int] = None,
            event_owner: Optional[str] = None,
            event_id: Optional[str] = None,
            status: Optional[str] = None
    ):
        query = select(event_invites)
        if pk:
            query = query.where(event_invites.c.id == pk)
        if user_id:
            query = query.where(event_invites.c.from_user == user_id)
        if event_owner:
            query = query.where(event_invites.c.to_user == event_owner)
        if event_id:
            query = query.where(event_invites.c.to_event == event_id)
        if status:
            query = query.where(event_invites.c.status == status)
        result = await database.fetch_one(query=query)
        return result

    @staticmethod
    async def create(event_id, to_user_id, from_user_id, _type: str = 'BET'):
        query = event_invites.insert()
        values = {
            'to_event': event_id,
            'to_user': to_user_id,
            'from_user': from_user_id,
            'status': InviteStatus.CREATED,
            'type': _type
        }
        return await database.execute(query=query, values=values)

    @database.transaction()
    async def request_to_join(self, event_id, to_user_id, from_user_id):
        invite = await self.create(event_id, to_user_id, from_user_id)
        message = Messages.EVENT_INVITE.value
        await MessagesService.create(from_user_id, to_user_id, message, event_id, invite, EVENT)
        await UserService.change_user_notifications_status(to_user_id, True)
        return invite

    @database.transaction()
    async def decline_to_participate_in(self, event_id, to_user_id, from_user_id):
        # Надо учесть 2 случая, когда запрос уже был принят и когда еще нет

        # Invite accepted already
        query = select([event_invites.c.id]).where(
            event_invites.c.from_user == from_user_id).where(
            event_invites.c.to_user == to_user_id,
            event_invites.c.to_event == event_id,
            event_invites.c.is_active.is_(True)
        )
        event_invite_id = await database.execute(query=query)
        if event_invite_id:
            query = event_invites.update().where(event_invites.c.id == event_invite_id).values(
                status=InviteStatus.RECALLED, is_active=False)
            await self._delete_event_user(event_id, from_user_id)
            await database.execute(query=query)
            message = Messages.EVENT_DECLINE.value
            await MessagesService.create(
                from_user_id, to_user_id, message, event_id, event_invite_id, EVENT)
            await UserService.change_user_notifications_status(to_user_id, True)

        # Invite not accepted yet

        # TODO  Invite not accepted yet

    @database.transaction()
    async def decline_invite(self, event, invites_id, sender, message_id, owner_id):
        query = event_invites.update().where(
            (event_invites.c.id == invites_id)
            & (event_invites.c.from_user == sender)
        ).values(status=InviteStatus.DECLINED, is_active=False)
        # delete MtM table event_users if exist
        await self._delete_event_user(event, sender)
        await database.execute(query=query)
        await MessagesService.change_message_status(list(message_id))
        message = Messages.REQUEST_REJECTED.value
        await MessagesService.create(
            owner_id, sender, message, event, invites_id, EVENT)
        await UserService.change_user_notifications_status(sender, True)

    @database.transaction()
    async def accept_invite(self, event_id, invites_id, sender, message_id, owner_id):
        query = event_invites.update().where(
            (event_invites.c.id == invites_id)
            & (event_invites.c.from_user == sender)
        ).values(status=InviteStatus.ACCEPTED)
        # create MtM table event_users
        await self._create_event_user(event_id, sender)
        await database.execute(query=query)
        await MessagesService.change_message_status(list(message_id))
        message = Messages.REQUEST_CONFIRM.value
        await MessagesService.create(
            owner_id, sender, message, event_id, invites_id, EVENT)
        await UserService.change_user_notifications_status(sender, True)

    @staticmethod
    async def _create_event_user(event, sender):
        # if exist
        e_u = select([event_users.c.id]).where(
            event_users.c.events_id == event).where(
            event_users.c.users_id == sender
        )
        if not await database.execute(query=e_u):
            query = event_users.insert()
            values = {
                'events_id': event,
                'users_id': sender
            }
            await database.execute(query=query, values=values)

    @staticmethod
    async def _delete_event_user(event, sender):
        query = event_users.delete().where(
            event_users.c.events_id == event).where(
            event_users.c.users_id == sender
        )
        await database.execute(query=query)

    @staticmethod
    async def is_show_event_invite_button(event, user):
        show_cancel_button = False
        show_invite_button = True
        show_processing_button = False
        participate_user = [d['id'] for d in event['members'] if 'id' in d]
        if user:
            if user['user_id'] in participate_user:
                show_cancel_button = True
                show_invite_button = False
            if user['user_id'] == event['creator']:
                show_invite_button = False
            if await InviteService.get(
                    user_id=user['user_id'],
                    event_owner=event['creator'],
                    event_id=event['id'],
                    status=InviteStatus.CREATED
            ):
                show_invite_button = False
                show_processing_button = True
        return show_cancel_button, show_invite_button, show_processing_button
