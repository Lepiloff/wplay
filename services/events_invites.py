from models.invites import event_invites, InviteStatus
from models.events import event_users
from models.messages import messages
from models.notifications import notifications
from services.notifications import NotificationsService
from services.messages import MessagesService
from db import database


EVENT = 'EVENT'


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

    async def request_to_join(self, event_id, to_user_id, from_user_id):
        # TODO обернуть в транзакцию или в try
        invite = await InviteService.create(event_id, to_user_id, from_user_id)
        await MessagesService.create(from_user_id, to_user_id, event_id, invite, EVENT)
        return invite

    async def decline_invite(self, event, event_id, sender):
        # TODO обернуть в транзакцию или в try
        query = event_invites.update().where(
            event_invites.c.id == event_id
        ).where(
            event_invites.c.from_user == sender
        ).values(status=InviteStatus.DECLINED)
        # delete MtM table event_users if exist
        await self.delete_event_user(event, sender)
        await database.execute(query=query)

    async def accept_invite(self, event_id, invites_id, sender):
        # TODO транзакция
        query = event_invites.update().where(
            event_invites.c.id == invites_id
        ).where(
            event_invites.c.from_user == sender).values(status=InviteStatus.ACCEPTED)
        print(query)
        await self.create_event_user(event_id, sender)
        await database.execute(query=query)

    @staticmethod
    async def create_event_user(event, sender):
        query = event_users.insert()
        values = {
            'events_id': event,
            'users_id': sender
        }
        await database.execute(query=query, values=values)

    @staticmethod
    async def delete_event_user(event, sender):
        query = event_users.delete().where(
            event_users.c.events_id == event).where(
            event_users.c.users_id == sender
        )
        await database.execute(query=query)


