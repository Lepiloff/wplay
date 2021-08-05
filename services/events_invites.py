from models.invites import event_invites
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
        # await NotificationsService.create(to_user_id, EVENT)
        await MessagesService.create(from_user_id, to_user_id, event_id, EVENT)
        return invite

    # async def send_request_for_invite(self, event_id, to_user_id, from_user_id):
    #     print (event_id, to_user_id)
    #     return event_id

    async def invite_processing(self):
        pass
