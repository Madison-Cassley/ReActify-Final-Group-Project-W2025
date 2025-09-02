# File: src/common/iot/__init__.py
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

import logging
from abc import ABC, abstractmethod
from typing import Callable

from common.devices.sensor import Reading

logger = logging.getLogger(__name__)


class IOTDeviceClient(ABC):
    """Abstract class defining common IOT integrations for the system.

    Attributes:
        callbacks (dict[str, Callable]): dictionary of key->callback pairs.
    """

    callbacks: dict[str, Callable]

    def __init__(self) -> None:
        """Contructor."""
        self.connected = False
        self.callbacks = {
            "control_actuator": lambda: logger.error(
                "No callback registered for 'control_actuator'"
            ),
            "set_telemetry_interval": lambda: logger.error(
                "No callback registered for 'set_telemetry_interval'"
            ),
        }

    def register_callback(self, key: str, callback: Callable) -> None:
        """Registers a named callback function.

        Args:
            key (str): the key to reference a given callback function
            callback (Callable): the callback
        """
        self.callbacks[key] = callback

    @abstractmethod
    async def connect(self) -> None:
        """Connects to IoTHub."""
        pass

    @abstractmethod
    async def send_reading(self, reading: Reading) -> None:
        """Sends reading to IoTHub."""
        pass

    @abstractmethod
    async def send_readings(self, readings: list[Reading]) -> None:
        """Sends readings to IoTHub."""
        pass
