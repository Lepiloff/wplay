import geocoder
import folium


class Map:
    def __init__(self, event_coordinate, zoom_start, popup=None, tooltip=None):
        self.event_coordinate = event_coordinate
        self.zoom_start = zoom_start
        self.popup = popup
        self.tooltip = tooltip

    def show_map(self):
        # Create the map
        return self.add_marker()

    def init_map(self):
        return folium.Map(location=self.event_coordinate, zoom_start=self.zoom_start)

    def add_marker(self):
        m = self.init_map()
        folium.Marker(
            location=list(self.event_coordinate),
            popup=self.popup,
            tooltip=self.tooltip,
            icon=folium.Icon(color="red", icon="info-sign")
        ).add_to(m)
        return m


