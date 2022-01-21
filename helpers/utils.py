import geocoder


def get_city():
    return geocoder.ip('me').city


def get_coord(country, city, street, house):
    # city = get_city()
    g = geocoder.osm(f'{country} {city} {street} {house}')
    if not g:
        raise Exception
    lat, lon = tuple(g.latlng)
    return lat, lon
