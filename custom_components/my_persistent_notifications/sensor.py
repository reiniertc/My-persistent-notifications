import logging
from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.typing import HomeAssistantType, ConfigType, DiscoveryInfoType

_LOGGER = logging.getLogger(__name__)

async def async_setup_platform(hass: HomeAssistantType, config: ConfigType, async_add_entities, discovery_info: DiscoveryInfoType = None):
    """Set up the persistent notifications sensor."""
    _LOGGER.info("🛎️ Persistent Notifications Sensor wordt geladen via async_setup_platform")
    async_add_entities([PersistentNotificationSensor(hass)], True)

class PersistentNotificationSensor(SensorEntity):
    def __init__(self, hass):
        self._hass = hass
        self._attr_name = "Persistent Notifications"
        self._attr_unique_id = "persistent_notifications_sensor"
        self._state = 0
        self._attr_extra_state_attributes = {"notifications": []}

    async def async_update(self):
        _LOGGER.debug("🔄 Sensor update gestart")

        ws_client = await self._hass.helpers.aiohttp_client.async_get_clientsession().__aenter__()
        ws = await ws_client.ws_connect("ws://localhost:8123/api/websocket")

        await ws.send_json({"type": "auth", "access_token": self._hass.data['auth'].access_token})
        await ws.receive_json()  # auth_ok
        await ws.send_json({"id": 1, "type": "persistent_notification/get"})
        response = await ws.receive_json()
        ws.close()

        if "result" in response:
            self._attr_extra_state_attributes["notifications"] = response["result"]
            self._state = len(response["result"])
        else:
            self._attr_extra_state_attributes["notifications"] = []
            self._state = 0
