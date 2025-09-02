# File: tests/example_system/conftest.py
# Project: final-project-upstream
# Creation date: 29 Apr 2025
# Author: michaelhaaf <michael.haaf@gmail.com>
# Modified By: Madison Cassley
# Changes made: added src. to the imports
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

import pytest
from gpiozero import OutputDevice
from gpiozero.pins.mock import MockFactory
from grove.grove_temperature_humidity_aht20 import GroveTemperatureHumidityAHT20

from src.common.devices.actuator import Actuator
from src.common.devices.device_controller import DeviceController
from src.common.devices.sensor import Sensor
from src.example_system.devices.aht20 import (
    HumiditySensor,
    MockGroveTemperatureHumidityAHT20,
    TemperatureSensor,
)
from src.example_system.devices.fan import FanActuator


@pytest.fixture
def mock_aht20() -> GroveTemperatureHumidityAHT20:
    """Fixture mocking a GroveTemperatureHumidityAHT20 device connected to i2c bus 4 of the reTerminal."""
    return MockGroveTemperatureHumidityAHT20(address=0x38, bus=4)


@pytest.fixture
def mock_fan() -> OutputDevice:
    """Fixture mocking a Fan connected to GPIO 16 on the grove base hat."""
    return OutputDevice(pin=16, pin_factory=MockFactory())


@pytest.fixture
def temperature_sensor(mock_aht20: GroveTemperatureHumidityAHT20) -> TemperatureSensor:
    """Fixture sensor for the TEMPERATURE measurement."""
    device = mock_aht20
    return TemperatureSensor(device=device)


@pytest.fixture
def humidity_sensor(mock_aht20: GroveTemperatureHumidityAHT20) -> HumiditySensor:
    """Fixture sensor for the HUMIDITY measurement."""
    device = mock_aht20
    return HumiditySensor(device=device)


@pytest.fixture
def fan_actuator(mock_fan: OutputDevice) -> FanActuator:
    """Fixture actuator for the FAN_TOGGLE action."""
    fan = mock_fan
    return FanActuator(device=fan)


@pytest.fixture
def all_actuators(
    fan_actuator: FanActuator,
) -> list[Actuator]:
    """A list of all available actuator fixtures."""
    return [fan_actuator]


@pytest.fixture
def all_sensors(
    temperature_sensor: TemperatureSensor,
    humidity_sensor: HumiditySensor,
) -> list[Sensor]:
    """A list of all available sensor fixtures."""
    return [temperature_sensor, humidity_sensor]


@pytest.fixture
def device_controller(
    all_actuators: list[Actuator], all_sensors: list[Sensor]
) -> DeviceController:
    """Fixture DeviceController instantiated with all available actuators and sensors."""
    return DeviceController(actuators=all_actuators, sensors=all_sensors)
