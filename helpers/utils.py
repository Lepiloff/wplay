import geocoder


def get_city():
    return geocoder.ip('me').city


def get_coord(street, house):
    city = get_city()
    g = geocoder.osm(f'{city} {street} {house}')
    if not g:
        raise Exception
    lat, lon = tuple(g.latlng)
    return lat, lon
