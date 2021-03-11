from db import database
from query import create_activity
from models.activities import activities


class ActivityService:
    async def post(self, name: str):
        values = {"name": name}
        return await database.execute(query=create_activity, values=values)

    async def get(self):
        result = await database.fetch_all(query=activities.select())
        result = [dict(r) for r in result]
        return result
