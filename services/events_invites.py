from sqlalchemy.sql.expression import select, exists

from db import database
from models.invites import event_invites, InviteStatus
from models.events import event_users
from models.messages import messages
from models.notifications import notifications
from services.notifications import NotificationsService
from services.messages import MessagesService
from services.user import UserService


EVENT = 'EVENT'

#TODO добавить функционал приглашения пользователя в ивент
# TODO статус 'CREATED'  почему не в константе находится

class InviteService:

    async def get(self):
        pass

    @staticmethod
    async def create(event_id, to_user_id, from_user_id, _type: str = 'BET'):
        query = event_invites.insert()
        values = {
            'to_event': event_id,
            'to_user': to_user_id,
            'from_user': from_user_id,
            'status': 'CREATED',
            'type': _type
        }
        return await database.execute(query=query, values=values)

    @database.transaction()
    async def request_to_join(self, event_id, to_user_id, from_user_id):
        invite = await self.create(event_id, to_user_id, from_user_id)
        await MessagesService.create(from_user_id, to_user_id, event_id, invite, EVENT)
        await UserService.change_user_notifications_status(to_user_id, True)
        return invite

    @database.transaction()
    async def decline_to_participate_in(self, event_id, to_user_id, from_user_id):
        # Надо учесть 2 случая, когда запрос уже был принят и когда еще нет


        pass

    @database.transaction()
    async def decline_invite(self, event, event_id, sender, message_id):
        query = event_invites.update().where(
            event_invites.c.id == event_id
        ).where(
            event_invites.c.from_user == sender
        ).values(status=InviteStatus.DECLINED)
        # delete MtM table event_users if exist
        await self._delete_event_user(event, sender)
        await database.execute(query=query)
        await MessagesService.change_message_status(message_id)

    @database.transaction()
    async def accept_invite(self, event_id, invites_id, sender, message_id):
        query = event_invites.update().where(
            event_invites.c.id == invites_id
        ).where(
            event_invites.c.from_user == sender).values(status=InviteStatus.ACCEPTED)
        # create MtM table event_users
        await self._create_event_user(event_id, sender)
        await database.execute(query=query)
        await MessagesService.change_message_status(message_id)

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


