import logging
from homeassistant.components.sensor import SensorEntity
from homeassistant.const import CONF_PLATFORM

_LOGGER = logging.getLogger(__name__)

CONF_FILTERS = "filters"

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up the persistent notification sensor."""
    filters = config.get(CONF_FILTERS, [])
    async_add_entities([PersistentNotificationSensor(hass, filters)], True)

class PersistentNotificationSensor(SensorEntity):
    """Sensor to track active persistent notifications."""

    def __init__(self, hass, filters):
        self._hass = hass
        self._filters = filters
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
            notifications = self._hass.data.get("persistent_notification", {})

            active = []
            for notif_id, notif in notifications.items():
                if not notif.get("dismissed", False):
                    active.append({
                        "id": notif_id,
                        "title": notif.get("title"),
                        "message": notif.get("message"),
                    })

            self._state = len(active)

            # Basisattribuut: alle notificaties
            attributes = {
                "notifications": active
            }

            # Filter tellers toevoegen
            for filter_prefix in self._filters:
                count = sum(1 for n in active if n["id"].startswith(filter_prefix))
                attributes[filter_prefix] = count

            self._attributes = attributes

        except Exception as e:
            _LOGGER.error("Fout bij ophalen meldingen: %s", e)
            self._state = 0
            self._attributes = {"error": str(e)}
