from models.notifications import notifications
from db import database
from query import get_user_notifications


# NOT USING NOW
class NotificationsService:

    @staticmethod
    async def create(recipient, _type):
        query = notifications.insert()
        values = {
            'recipient': recipient,
            'type': _type
        }
        return await database.execute(query=query, values=values)

    @staticmethod
    async def get(user_id):
        result = await database.fetch_all(query=get_user_notifications, values={'user': str(user_id)})
        result = [dict(r) for r in result]
        return result

