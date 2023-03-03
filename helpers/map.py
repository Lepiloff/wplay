import aiohttp

import ipinfo
import folium

from helpers.utils import get_settings


#TODO async ?
class Map:
    def __init__(self, event_coordinate=None, zoom_start=15, popup=None, tooltip=None):
        self.session = None
        self.event_coordinate = event_coordinate
        self.zoom_start = zoom_start
        self.popup = popup
        self.tooltip = tooltip

    @staticmethod
    async def _get_city_center_coord():
        async with aiohttp.ClientSession() as session:
            access_token = get_settings().ipinfo_access_token
            handler = ipinfo.AsyncHandler(access_token, session=session)
            details = await handler.getDetails()
            lat, lon = (details.latitude, details.longitude)
        return lat, lon

    async def show_event(self):
        return await self._add_marker(await self._init_map())

    async def show_events(self, event_list):
        m = await self._init_map()
        for event in event_list:
            id, popup, lat, long, tooltip = event
            folium.Marker(
                location=list((lat, long)),
                popup=popup,
                tooltip=tooltip,
                icon=folium.Icon(color="red", icon="info-sign")
            ).add_to(m)
        return m

    async def _init_map(self):
        if self.session is None:
            self.session = aiohttp.ClientSession()
        with self.session:
            if self.event_coordinate:
                return folium.Map(location=self.event_coordinate, zoom_start=self.zoom_start)
            else:
                lat, lon = await self._get_city_center_coord()
                return folium.Map(
                    location=list((lat, lon)),
                    zoom_start=self.zoom_start
                )

    async def _add_marker(self, m):
        folium.Marker(
            location=list(self.event_coordinate),
            popup=self.popup,
            tooltip=self.tooltip,
            icon=folium.Icon(color="red", icon="info-sign")
        ).add_to(m)
        return m


