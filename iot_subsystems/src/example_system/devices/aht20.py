# File: src/example_system/devices/aht20.py
# Project: final-project-upstream
# Creation date: 29 Apr 2025
# Author: michaelhaaf <michael.haaf@gmail.com>
# Modified By: N/A
# Changes made: N/A
# -----
# This software is intended for educational use by students and teachers in the
# the Computer Science department at John Abbott College.
# See the license disclaimer below and the project LICENSE file for more information.
# -----
# Copyright (C) 2025 michaelhaaf
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

import contextlib
import logging
from random import random
from time import sleep

from grove.grove_temperature_humidity_aht20 import GroveTemperatureHumidityAHT20

from common.devices.sensor import Measurement, Reading, Sensor

logger = logging.getLogger(__name__)


class MockGroveTemperatureHumidityAHT20(GroveTemperatureHumidityAHT20):
    """Mock implementation of the GroveTemperatureHumidityAHT20."""

    def __init__(self, address: int = 0x38, bus: int = 4) -> None:
        """Initializes the mock class."""
        self.address = address
        self.bus = bus

    def read(self) -> tuple[float, float]:
        """Returns a random reading between 0-100 for temperature and humidity."""
        return (random() * 100, random() * 100)


class TemperatureSensor(Sensor):
    """Implementation of Sensor for taking Temperature measurements."""

    device: GroveTemperatureHumidityAHT20
    measurement: Measurement

    def __init__(self, device: GroveTemperatureHumidityAHT20) -> None:
        """TemperatureSensor constructor."""
        self.device = device
        self.measurement = Measurement.TEMPERATURE

    def read_sensor(self) -> Reading:
        """See base class."""
        temperature, _ = self.device.read()
        reading = Reading(value=temperature, measurement=self.measurement)
        logger.info(reading)
        return reading


class HumiditySensor(Sensor):
    """Implementation of Sensor class for taking Humidity measurements."""

    device: GroveTemperatureHumidityAHT20
    measurement: Measurement

    def __init__(self, device: GroveTemperatureHumidityAHT20) -> None:
        """HumiditySensor constructor."""
        self.device = device
        self.measurement = Measurement.HUMIDITY

    def read_sensor(self) -> Reading:
        """See base class."""
        _, humidity = self.device.read()
        reading = Reading(value=humidity, measurement=self.measurement)
        logger.info(reading)
        return reading


def main() -> None:
    """Routine for testing aht20 sensors when this file is run as a script rather than a module.
    Useful pattern when you want to test a single device in isolation.

    Usage:
        $ PYTHONPATH=src:${PYTHONPATH} python src/example_system/devices/aht20.py
    Alternatively:
        $ export PYTHONPATH=${HOME}/path-to-repository/src:${PYTHONPATH}
        $ python src/example_system/devices/aht20.py
    """
    device = GroveTemperatureHumidityAHT20(bus=4)
    humi_sensor = TemperatureSensor(device=device)
    temp_sensor = HumiditySensor(device=device)
    while True:
        logger.info(temp_sensor.read_sensor())
        logger.info(humi_sensor.read_sensor())
        sleep(1)


if __name__ == "__main__":
    with contextlib.suppress(KeyboardInterrupt):
        main()
