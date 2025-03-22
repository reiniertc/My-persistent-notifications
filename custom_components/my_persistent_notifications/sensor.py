import logging
from homeassistant.components.sensor import SensorEntity

_LOGGER = logging.getLogger(__name__)

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up the persistent notification sensor."""
    async_add_entities([PersistentNotificationSensor(hass)], True)

class PersistentNotificationSensor(SensorEntity):
    """Sensor to track active persistent notifications."""

    def __init__(self, hass):
        self._hass = hass
        self._state = 0
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
        """Update the sensor state."""
        try:
            # Haal meldingen op via Home Assistant helper
            notifications = self._hass.data.get("persistent_notification")

            if not notifications:
                self._state = 0
                self._attributes = {"notifications": []}
                return

            active = []
            for notif_id, notif in notifications.items():
                if not notif.get("dismissed", False):
                    active.append({
                        "id": notif_id,
                        "title": notif.get("title"),
                        "message": notif.get("message"),
                    })

            self._state = len(active)
            self._attributes = {
                "notifications": active
            }

        except Exception as e:
            _LOGGER.error("Fout bij ophalen meldingen: %s", e)
            self._state = 0
            self._attributes = {"error": str(e)}
