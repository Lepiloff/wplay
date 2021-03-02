from db import database
from query import create_activity
from models.activities import activities


async def post(name):
    values = {"name": name}
    return await database.execute(query=create_activity, values=values)


async def get():
    result = await database.fetch_all(query=activities.select())
    result = [dict(r) for r in result]
    return result
