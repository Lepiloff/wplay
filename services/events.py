import ast
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
    EVENT_CONTENT = ('location', 'activity')

    async def get(self, pk: int):
        # TODO убрать из query файла SQL запрс в виде функции и заменить на  передачу параметров с помощью ":"
        result = await database.fetch_one(text(get_event(pk)))
        if result is None:
            raise HTTPException(status_code=404, detail="Events not found")
        event = dict(result.items())
        # event['location'] = ast.literal_eval(event['location'])
        # event['activity'] = ast.literal_eval(event['activity'])
        event['location'] = json.loads(event['location'])
        event['activity'] = json.loads(event['activity'])
        return event

    async def get_list(self):
        db_result = await database.fetch_all(get_events)
        if db_result is None:
            raise HTTPException(status_code=404, detail="Events not found")
        result = ([dict(r.items()) for r in db_result])
        events = []
        for event in result:
            #TODO вынести список атрибутов event в отдельную константу
            # e = {k: ast.literal_eval(v) if k in ('location', 'activity') else v for k, v in event.items()}
            e = {k: json.loads(v) if k in ('location', 'activity') else v for k, v in event.items()}
            events.append(e)
        return events

    async def post(self, user_id, street, house,
                   title, content, activity,
                   is_private, start_date, start_time):
        # TODO  в transaction завернуть ?
        lat, lon = get_coord(street, house)
        values = {'city': get_city(), 'street': street,
                  'house': house, 'lat': lat, 'long': lon
                  }

        #TODO не создавать а возвращать локацию если такая уже существует
        location_id = await database.execute(query=location_create, values=values)
        values = {'creator': user_id, 'title': title, 'content': content,
                  'location_id': int(location_id), 'activities_id': int(activity),
                  'is_private': is_private, 'start_date': start_date, 'start_time': start_time
                  }
        print (values)
        print (type(values["start_time"]))
        event_id = await database.execute(query=event_create, values=values)
        return dict(await database.fetch_one(get_event(event_id)))
    # TODO добавить update метод

