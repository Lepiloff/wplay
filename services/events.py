import json
from typing import Dict

from fastapi import HTTPException

from db import database
from helpers.utils import get_coord
from query import get_event, get_events, location_create, event_create, event_user_create


class EventsService:

    async def get(self, pk: int):
        result = await database.fetch_one(query=get_event, values={'pk': pk})
        if result is None:
            raise HTTPException(status_code=404, detail="Event not found")
        event = dict(result)
        return self.perform_data(event)

    async def get_list(self):
        db_result = await database.fetch_all(get_events)
        if db_result is None:
            raise HTTPException(status_code=404, detail="Events not found")
        result = ([dict(r) for r in db_result])
        return list(map(self.perform_data, result))

    @database.transaction()
    async def post(self, user_id, country, city, street, house,
                   title, content, activity, members_count,
                   is_private, start_date, start_time):
        lat, lon = await get_coord(country, city, street, house)
        values = {'country': country, 'city': city, 'street': street,
                  'house': house, 'lat': lat, 'long': lon
                  }

        #TODO не создавать а возвращать локацию если такая уже существует
        location_id = await database.execute(query=location_create, values=values)
        values = {
            'creator': user_id, 'title': title, 'content': content,
            'location_id': int(location_id), 'activities_id': int(activity), 'members_count': members_count,
            'is_private': is_private, 'start_date': start_date, 'start_time': start_time
                  }
        event_id = await database.execute(query=event_create, values=values)
        return event_id

    @staticmethod
    def perform_data(data: Dict):
        """
        Response from DB came as a json, rewrite it to dict for template using
        """
        key_for_perform = ('location', 'activity', 'creator_info', 'members')
        ready_data = {
            key: json.loads(value)
            if key in key_for_perform
            else value for key, value
            in data.items()
        }
        return ready_data
