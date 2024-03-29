from geopy.adapters import AioHTTPAdapter
from geopy.geocoders import Nominatim, GoogleV3
import urllib
from functools import lru_cache

from fastapi import Request, Response
from typing import Any, Dict
import sqlalchemy.types as types

from config import Settings
from helpers.constants import EventNotification


class EnumAsInteger(types.TypeDecorator):
    """Column type for storing Python enums in a database INTEGER column.

    This will behave erratically if a database value does not correspond to
    a known enum value.
    https://stackoverflow.com/a/38786737/9262339
    """
    impl = types.Integer

    def __init__(self, enum_type):
        super(EnumAsInteger, self).__init__()
        self.enum_type = enum_type

    def process_bind_param(self, value, dialect):
        if isinstance(value, self.enum_type):
            return value.value
        raise ValueError('expected %s value, got %s'
                         % (self.enum_type.__name__, value.__class__.__name__))

    def process_result_value(self, value, dialect):
        return self.enum_type(value)

    def copy(self, **kwargs):
        return EnumAsInteger(self.enum_type)


class CustomURLProcessor:
    """fastapi не может обрабатывать query параметры переданные в шаблоне jinja
      Этот класс фиксит проблему (в следующих  версиях starlette возможно подфиксят)
    """
    def __init__(self):
        self.path = ""
        self.request = None

    def url_for(self, request: Request, name: str, **params: str):
        self.path = request.url_for(name, **params)
        self.request = request
        return self

    def include_query_params(self, **params: str):
        parsed = list(urllib.parse.urlparse(self.path))
        parsed[4] = urllib.parse.urlencode(params)
        return urllib.parse.urlunparse(parsed)


async def get_coord(country, city, street, house):
    # Try to get coordinate using free Nominatim, else try with GoogleV3 (paid)
    async with Nominatim(
            user_agent='wonna_train',
            adapter_factory=AioHTTPAdapter,
    ) as geolocator:
        location = await geolocator.geocode(f'{country} {city} {street} {house}', timeout=10)
    try:
        lat, lon = (location.latitude, location.longitude)
    except AttributeError:
        async with GoogleV3(
                api_key=get_settings().google_maps_api_key,
                adapter_factory=AioHTTPAdapter
        ) as geolocator:
            location = await geolocator.geocode(f'{country} {city} {street} {house}', timeout=10)
            lat, lon = (location.latitude, location.longitude)
    return lat, lon


async def str_to_int(data: Dict) -> Dict:
    return {key: (int(value) if value.isdigit() else value) for key, value in data.items()}


async def bool_to_int(data: Dict) -> Dict:
    return {key: (int(value) if isinstance(value, bool) else value) for key, value in data.items()}


@lru_cache()
def get_settings():
    return Settings()


async def add_event_message_to_response(response: Response, result: bool) -> Response:
    message = EventNotification.SUCCESS.value if result else EventNotification.NOT_SUCCESS.value
    response.set_cookie(
        'event_notifications',
        value=message,
        httponly=True,
        max_age=3,
        expires=3,
    )
    return response
