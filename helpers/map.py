import aiohttp

import ipinfo
import folium

from helpers.utils import get_settings


#TODO async ?
class Map:
    def __init__(self, event_coordinate=None, zoom_start=15, popup=None, tooltip=None):
        self.event_coordinate = event_coordinate
        self.zoom_start = zoom_start
        self.popup = popup
        self.tooltip = tooltip

    async def _get_city_center_coord(self):
        async with ipinfo.getHandlerAsync(get_settings().ipinfo_access_token) as handler:
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
        if self.event_coordinate:
            return folium.Map(location=self.event_coordinate, zoom_start=self.zoom_start)
        else:
            return folium.Map(
                location=await self._get_city_center_coord(),
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




