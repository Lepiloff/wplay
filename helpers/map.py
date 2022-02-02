import geocoder
import folium

#TODO async ?
class Map:
    def __init__(self, event_coordinate=None, zoom_start=15, popup=None, tooltip=None):
        self.event_coordinate = event_coordinate
        self.zoom_start = zoom_start
        self.popup = popup
        self.tooltip = tooltip


    @staticmethod
    def get_city_center_coord():
        # TODO точность хромает, рассмотреть другой способ получения координат
        g = geocoder.ip('me')
        country, city = (g.country, g.city)
        g = geocoder.osm(f'{country} {city}')
        if not g:
            raise Exception
        lat, lon = tuple(g.latlng)
        return lat, lon

    def show_event(self):
        return self.add_marker(self.init_map())

    def show_events(self, event_list):
        m = self.init_map()
        for event in event_list:
            id, popup, lat, long, tooltip = event
            folium.Marker(
                location=list((lat, long)),
                popup=popup,
                tooltip=tooltip,
                icon=folium.Icon(color="red", icon="info-sign")
            ).add_to(m)
        return m

    def init_map(self):
        if self.event_coordinate:
            return folium.Map(location=self.event_coordinate, zoom_start=self.zoom_start)
        else:
            return folium.Map(location=self.get_city_center_coord(), zoom_start=self.zoom_start)

    def add_marker(self, m):
        folium.Marker(
            location=list(self.event_coordinate),
            popup=self.popup,
            tooltip=self.tooltip,
            icon=folium.Icon(color="red", icon="info-sign")
        ).add_to(m)
        return m


