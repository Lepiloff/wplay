from models.invites import event_invites
from db import database


class InviteService:
    async def get(self):
        pass

    @staticmethod
    async def invite_create(event_id, to_user_id, from_user_id):
        query = event_invites.insert()
        values = {
            'to_event': event_id,
            'to_user': to_user_id,
            'from_user': from_user_id,
            'status': 'CREATED',
            'type': 'BET'
        }
        return await database.execute(query=query, values=values)

    async def request_to_join(self, event_id, to_user_id, from_user_id):
        invite = await InviteService.invite_create(event_id, to_user_id, from_user_id)
        return invite

    # async def send_request_for_invite(self, event_id, to_user_id, from_user_id):
    #     print (event_id, to_user_id)
    #     return event_id

    async def invite_processing(self):
        pass
