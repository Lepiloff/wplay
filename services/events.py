import itertools
import json

from sqlalchemy import select, desc, column, func, table, and_, text

from fastapi import HTTPException

from db import database
from helpers.utils import get_city, get_coord
from models.users import users
from models.events import events
from models.locations import locations
from models.activities import activities
from query import get_event, get_events, location_create, event_create, event_user_create


class EventsService:

    async def get(self, pk: int):
        result = await database.fetch_one(text(get_event(pk)))
        if result is None:
            raise HTTPException(status_code=404, detail="Events not found")
        return dict(result)
        # TODO снизу работает все ок, но не группирует foreignkey в один объект, прочекать эту возможность
        # query = (
        #     select(
        #         [
        #             func.json_build_object(
        #                 "id",
        #                 events.c.id,
        #                 "title",
        #                 events.c.title,
        #                 "location",
        #                 func.json_agg(
        #                     func.json_build_object(
        #                         "city",
        #                         locations.c.city,
        #                         "street",
        #                         locations.c.street,
        #                         "building",
        #                         locations.c.building,
        #                     )
        #                 ),
        #                 "location_all_columns_example",
        #                 func.json_agg(func.json_build_object(
        #                     *itertools.chain(*[(_.name, _) for _ in locations.c])
        #                 )),
        #                 "activity",
        #                 func.json_agg(
        #                     func.json_build_object(
        #                         "name",
        #                         activities.c.name,
        #                     )
        #                 ),
        #             )
        #         ]
        #     )
        #         .select_from(events.join(locations).join(activities))
        #         .where(
        #         and_(
        #             events.c.id == pk,
        #             locations.c.id == events.c.location_id,
        #             activities.c.id == events.c.activities_id,
        #         )
        #     )
        #         .order_by(desc(events.c.created_at))
        #         .group_by(events.c.id)  # !!! <- IMPORTANT
        # )
        # print(query)
        # ev = dict(await database.fetch_one(query))
        # if ev is None:
        #     raise HTTPException(status_code=404, detail="Event not found")
        #
        # print(ev)

        # return ev

    async def get_list(self):
        db_result = await database.fetch_all(get_events)
        result = ([dict(r) for r in db_result])
        result = [{k: json.loads(v) for k, v in r.items()} for r in result]
        # events_list = await database.fetch_all(query=events.select())
        #
        # if events_list is not None:
        #     return [dict(event) for event in events_list]
        return result


    async def post(self, street, house, title, content, activity):
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
        # надо прочекать что необходимо и как это вернуть при создании объекта
        return dict(await database.fetch_one(get_event(event_id)))
    # TODO добавить update метод
