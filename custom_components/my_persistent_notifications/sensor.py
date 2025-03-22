import asyncio
import logging
import aiohttp
import json

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

LOGGER = logging.getLogger(__name__)

WEBSOCKET_URL = "ws://homeassistant.local:8123/api/websocket"

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback):
    """Setup sensor from config entry."""
    async_add_entities([PersistentNotificationSensor(hass)], True)

class PersistentNotificationSensor(SensorEntity):
    def __init__(self, hass: HomeAssistant):
        self.hass = hass
        self._state = 0
        self._attr_name = "Persistent Notifications"
        self._attr_unique_id = "persistent_notifications_sensor"
        self._attr_extra_state_attributes = {"notifications": []}

    async def async_update(self):
        """Fetch persistent notifications."""
        async with aiohttp.ClientSession() as session:
            async with session.ws_connect(WEBSOCKET_URL) as ws:
                await ws.send_json({"type": "auth", "access_token": self.hass.data["auth"].access_token})
                await ws.send_json({"id": 1, "type": "persistent_notification/get"})
                
                async for msg in ws:
                    data = json.loads(msg.data)
                    if "result" in data:
                        self._attr_extra_state_attributes["notifications"] = data["result"]
                        self._state = len(data["result"])
                        break

        self.async_write_ha_state()
