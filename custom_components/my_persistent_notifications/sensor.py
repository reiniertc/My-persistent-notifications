import logging
from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.aiohttp_client import async_get_clientsession

_LOGGER = logging.getLogger(__name__)

API_ENDPOINT = "/api/persistent_notification"

class PersistentNotificationSensor(SensorEntity):
    """Sensor that shows the number of active persistent notifications."""

    def __init__(self, hass):
        """Initialize the sensor."""
        self._hass = hass
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
        """Fetch persistent notifications from the Home Assistant API."""
        try:
            session = async_get_clientsession(self._hass)
            url = f"{self._hass.config.api.base_url}{API_ENDPOINT}"

            headers = {
                "Authorization": f"Bearer {self._hass.data['my_persistent_notifications_token']}",
                "Content-Type": "application/json",
            }

            async with session.get(url, headers=headers) as response:
                if response.status != 200:
                    _LOGGER.error("Error fetching notifications, status: %s", response.status)
                    self._state = 0
                    self._attributes = {"error": f"Status {response.status}"}
                    return

                data = await response.json()

                self._state = len(data)
                self._attributes = {
                    "notifications": data
                }

        except Exception as e:
            _LOGGER.error("Exception while fetching persistent notifications: %s", e)
            self._state = 0
            self._attributes = {
                "error": str(e)
            }
