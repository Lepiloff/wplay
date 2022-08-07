import geocoder
import urllib
from fastapi import Request
import sqlalchemy.types as types


def get_city():
    return geocoder.ip('me').city


def get_coord(country, city, street, house):
    g = geocoder.osm(f'{country} {city} {street} {house}')
    if not g:
        # TODO возвращать пользователю сообщение что адрес не корректен
        raise Exception('Location info not find')
    lat, lon = tuple(g.latlng)
    return lat, lon


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
