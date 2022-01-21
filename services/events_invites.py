from models.invites import event_invites, InviteStatus
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

    @staticmethod
    async def decline_invite(event_id):
        query = event_invites.update().where(event_invites.c.id == event_id).values(status=InviteStatus.DECLINED)
        await database.execute(query=query)

    @staticmethod
    async def accept_invite(event_id):
        query = event_invites.update().where(event_invites.c.id == event_id).values(status=InviteStatus.ACCEPTED)
        await database.execute(query=query)

