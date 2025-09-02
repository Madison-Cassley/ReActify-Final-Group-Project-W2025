# File: tests/example_system/conftest.py
# Project: final-project-upstream
# Creation date: 29 Apr 2025
# Author: michaelhaaf <michael.haaf@gmail.com>
# Modified By: Madison Cassley
# Changes made: added src. to the imports. replaced pytests with my own sensors/actuators
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

import os
import pytest

@pytest.fixture(autouse=True)
def set_test_env(monkeypatch):
    monkeypatch.setenv("ENVIRONMENT", "DEVELOPMENT")
    monkeypatch.setenv("IOTHUB_CONNECTION_STRING", "HostName=fake;DeviceId=fake;SharedAccessKey=fake")

from src.water_floods_subsystem.devices.soil_moisture import SoilMoistureSensor
from src.water_floods_subsystem.devices.water_level import WaterLevelSensor
from src.water_floods_subsystem.devices.servo_motor import ServoActuator
from src.water_floods_subsystem.devices.buzzer import BuzzerActuator

from src.common.devices.device_controller import DeviceController
from src.common.devices.sensor import Sensor
from src.common.devices.actuator import Actuator

def soil_sensor() -> SoilMoistureSensor:
    return SoilMoistureSensor(pin=0)

@pytest.fixture
def water_sensor() -> WaterLevelSensor:
    return WaterLevelSensor(pin=2)

@pytest.fixture
def servo_actuator() -> ServoActuator:
    return ServoActuator(pin=18)

@pytest.fixture
def buzzer_actuator() -> BuzzerActuator:
    return BuzzerActuator()

@pytest.fixture
def all_sensors(soil_sensor: SoilMoistureSensor, water_sensor: WaterLevelSensor) -> list[Sensor]:
    return [soil_sensor, water_sensor]

@pytest.fixture
def all_actuators(servo_actuator: ServoActuator, buzzer_actuator: BuzzerActuator) -> list[Actuator]:
    return [servo_actuator, buzzer_actuator]

@pytest.fixture
def device_controller(all_sensors: list[Sensor], all_actuators: list[Actuator]) -> DeviceController:
    return DeviceController(sensors=all_sensors, actuators=all_actuators)
