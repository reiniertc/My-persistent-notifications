import logging
from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from .const import DOMAIN, CONF_API_TOKEN

_LOGGER = logging.getLogger(__name__)
API_ENDPOINT = "/api/persistent_notification"

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up the sensor platform."""
    token = config.get(CONF_API_TOKEN)
    if not token:
        _LOGGER.error("No API token provided in configuration.yaml!")
        return

    async_add_entities([PersistentNotificationSensor(hass, token)], True)

class PersistentNotificationSensor(SensorEntity):
    def __init__(self, hass, token):
        self._hass = hass
        self._token = token
        self._state = None
        self._attributes = {}

    @property
    def name(self):
        return "Active Persistent Notifications"

    @property
    def state(self):
        return self._state

    @property
    def extra_state_attributes(self):
        return self._attributes

    async def async_update(self):
        session = async_get_clientsession(self._hass)
        url = f"{self._hass.config.api.base_url}{API_ENDPOINT}"

        headers = {
            "Authorization": f"Bearer {self._token}",
            "Content-Type": "application/json",
        }

        try:
            async with session.get(url, headers=headers) as response:
                if response.status != 200:
                    _LOGGER.error("API error: %s", response.status)
                    self._state = 0
                    self._attributes = {"error": f"HTTP {response.status}"}
                    return

                data = await response.json()
                self._state = len(data)
                self._attributes = {
                    "notifications": data
                }

        except Exception as e:
            _LOGGER.exception("Failed to fetch notifications: %s", e)
            self._state = 0
            self._attributes = {"error": str(e)}
