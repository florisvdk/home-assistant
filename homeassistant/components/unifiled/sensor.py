"""Platform for sensor integration."""
import logging

from homeassistant.const import POWER_WATT
from homeassistant.helpers.entity import Entity

from .const import DOMAIN, KEY_API

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, config_entry, async_add_devices):
    """Set up the Unifi LED platform."""

    api = hass.data[KEY_API][config_entry.entry_id]

    async_add_devices(UnifiLedSensor(light, api) for light in api.get_lights())


class UnifiLedSensor(Entity):
    """Representation of an unifiled."""

    def __init__(self, sensor, api):
        """Initialize the sensor."""
        self._api = api
        self._sensor = sensor
        self._unique_id = sensor["id"]
        self._name = sensor["name"]
        self._available = sensor["isOnline"]
        self._state = sensor["status"]["power"] / 1000

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def device_info(self):
        """Return the device info of this light."""
        return {
            "identifiers": {(DOMAIN, self._unique_id)},
            "name": self._name,
            "manufacturer": "Ubiquiti Networks",
            "model": self._sensor["info"]["model"],
            "sw_version": self._sensor["info"]["version"],
        }

    @property
    def available(self):
        """Return the available state of this sensor."""
        return self._available

    @property
    def unique_id(self):
        """Return the unique id of this light."""
        return self._unique_id

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return POWER_WATT

    def update(self):
        """Fetch new state data for the sensor."""
        temp = self._api.get_lights()
        for device in temp:
            if device["id"] == self._unique_id:
                self._state = device["status"]["power"] / 1000
