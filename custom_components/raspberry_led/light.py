"""Control LEDs on the raspberry"""
import logging

import homeassistant.helpers.config_validation as cv
from homeassistant.components.light import (
    ATTR_BRIGHTNESS, PLATFORM_SCHEMA, Light)

_LOGGER = logging.getLogger(__name__)


def setup_platform(hass, config, add_entities, discovery_info=None):
    _LOGGER.debug("setup platform", hass, config, add_entities, discovery_info)
    add_entities([RpiLED("green", "led0"), RpiLED("red", "led1")])


class RpiLED(Light):
    def __init__(self, color, path):
        self.unique_id = f"rpi_led_{color}"
        self._name = f"{color} LED"
        self._path = path
        self._state = None

    @property
    def name(self):
        return self._name

    @property
    def is_on(self):
        return self._state

    @property
    def path(self):
        return f"/sys/class/leds/{self._path}/brightness"

    def turn_on(self, **kwargs):
        with open(self.path, "w") as fd:
            fd.write("1")

    def turn_off(self, **kwargs):
        with open(self.path, "w") as fd:
            fd.write("0")

    def update(self):
        with open(self.path) as fd:
            brightness = fd.read().strip()
            self._state = brightness != "0"
