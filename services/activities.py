from db import database
from query import create_activity
from models.activities import activities


class ActivityService:
    async def post(self, name: str):
        return await database.execute(query=create_activity, values={"name": name})

    @staticmethod
    async def get():
        result = await database.fetch_all(query=activities.select())
        result = [dict(r) for r in result]
        return result
