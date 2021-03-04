import json
from fastapi import HTTPException

from db import database
from helpers.utils import get_city, get_coord
from models.users import users
from query import get_event, get_events, location_create, event_create, event_user_create


async def get(pk: int):
    result = await database.fetch_one(get_event(pk))
    if result is None:
        raise HTTPException(status_code=404, detail="Events not found")
    return dict(result)


async def get_all():
    db_result = await database.fetch_all(get_events)
    result = ([dict(r) for r in db_result])
    result = [{k: json.loads(v) for k, v in r.items()} for r in result]
    return result


async def post(street, house, title, content, activity):
    # TODO прочекать sql create relation tables in one query  а то чет много запросов
    lat, lon = get_coord(street, house)
    values = {"city": get_city(), "street": street, "house": house, "lat": lat, "long": lon}
    location_id = await database.execute(query=location_create, values=values)

    # TODO get current user
    user_query = users.select()
    user = await database.fetch_one(query=user_query)
    user_id = dict(user)["id"]

    values = {"creator": user_id, "title": title, "content": content,
              "location_id": int(location_id), "activities_id": int(activity)}
    event_id = await database.execute(query=event_create, values=values)
    values = {"events_id": int(event_id), "users_id": int(user_id)}
    await database.execute(query=event_user_create, values=values)
    # TODO сейчас сделано так что возвращает абсолютно все по ивенту, причем лишним запросом в базу.
    # адо прочекать что необходимо и как это вернуть при создании объекта
    return dict(await database.fetch_one(get_event(event_id)))
