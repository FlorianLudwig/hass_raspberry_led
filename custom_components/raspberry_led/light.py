"""Control LEDs on the raspberry"""
from typing import Optional
import logging

import homeassistant.helpers.config_validation as cv
from homeassistant.components.light import (
    ATTR_BRIGHTNESS, PLATFORM_SCHEMA, Light)

_LOGGER = logging.getLogger(__name__)


def setup_platform(hass, config, add_entities, discovery_info=None):
    _LOGGER.debug("setup platform", hass, config, add_entities, discovery_info)
    add_entities([RpiLED("green", "led0"), RpiLED("red", "led1")])


class RpiLED(Light):
    def __init__(self, color:str, path:str):
        self._color = color
        self._path = path
        self._state:Optional[bool] = None

    @property
    def unique_id(self) -> str:
        return f"rpi_led_{self._color}"

    @property
    def name(self) -> str:
        return f"{self._color} LED"

    @property
    def is_on(self) -> bool:
        return self._state

    @property
    def path(self) -> str:
        return f"/sys/class/leds/{self._path}/brightness"

    def turn_on(self, **kwargs) -> None:
        with open(self.path, "w") as fd:
            fd.write("1")

    def turn_off(self, **kwargs) -> None:
        with open(self.path, "w") as fd:
            fd.write("0")

    def update(self) -> None:
        with open(self.path) as fd:
            brightness = fd.read().strip()
            self._state = brightness != "0"
