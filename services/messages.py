from models.messages import messages
from db import database
from query import get_message_count


class MessagesService:

    @staticmethod
    async def create(sender, recipient, event_id, _type):
        query = messages.insert()
        content = f'You are recieved invoice from user {sender} to join event {event_id}'
        values = {
            'recipient': recipient,
            'sender': sender,
            'content': content,
            'type': _type,
        }
        return await database.execute(query=query, values=values)

    @staticmethod
    async def get_count(user_id):
        result = await database.fetch_one(query=get_message_count, values={'user_id': user_id})
        print(f'Result {result}')
        return dict(result) if result else None
