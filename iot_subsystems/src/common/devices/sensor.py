# File: src/common/devices/sensor.py
# Project: final-project-upstream
# Creation date: 29 Apr 2025
# Author: michaelhaaf <michael.haaf@gmail.com>
# Modified By: Madison Cassley
# Changes made: Added more sensors to the enum
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

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Any


class Measurement(dict, Enum):
    """Enum defining valid sensor measurements and their units of measurement.

    Supports JSON serialization by overriding dict.

    Used by the Reading and Sensor classes to distinguish readings and source sensors.

    Attributes:
        description (str): String describing the purpose and source device of the source measurement
        unit (str): String representing the unit of measurement.
        name (str): String that is the unique name of the measurement.
    """

    TEMPERATURE = {"unit": "°C", "description": "temperature in degrees celsius"}
    HUMIDITY = {"unit": "%RH", "description": "relative measurement of humidity"}
    SOIL_MOISTURE = {"unit": "%",  "description": "soil moisture level"} 
    WATER_LEVEL    = {"unit": "cm", "description": "water level"} 
    
    SOUND = {"unit": "boolean", "description": "sound detected (1) or not (0)"}
    MOTION = {"unit": "boolean", "description": "motion detected (1) or not (0)"}
    CO2LEVEL ={"unit": "ppm", "description": "co2 level"}


    def __init__(self, items: dict[str, str]) -> None:
        """Initialize the Measurement instance.

        Args:
            items (dict[str]): the dictionary to initialize the Measurement from.
                                Note: requires "unit" and "description" keys.
        """
        self.description = items["description"]
        self.unit = items["unit"]
        super().__init__({"name": self.name} | items)


@dataclass
class Reading:
    """Class for creating sensor readings.

    Attributes:
        value (str): the string representation of the value of the measurement. Can be quantitative or qualitative.
        measurement (Measurement): a measurement that the reading captures
    """

    value: str
    measurement: Measurement


class Sensor(ABC):
    """Abstract class providing a common interface to GPIO sensors.

    Attributes:
        device (Any): the eternal module used to capture sensor readings
        measurement (Measurement): the measurement type that the sensor is programmed to create readings of.
    """

    device: Any
    measurement: Measurement

    @abstractmethod
    def read_sensor(self) -> Reading:
        """Capture a sensor reading.

        Returns:
            a reading object matching the measurement type of the sensor containing the value measured by the sensor.
        """
        pass
