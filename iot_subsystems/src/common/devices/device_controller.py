# File: src/common/devices/device_controller.py
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

from common.devices.actuator import Actuator, Command
from common.devices.sensor import Measurement, Reading, Sensor

logger = logging.getLogger(__name__)


class DeviceController:
    """Class providing an overall interface for a system's set of actuators and sensors.

    Attributes:
        sensors (list[Sensor]): the list of sensors controlled by the device controller
        actuators (list[Actuator]): the list of actuators controlled by the device controller
    """

    sensors: list[Sensor]
    actuators: list[Actuator]

    def __init__(self, sensors: list[Sensor], actuators: list[Actuator]) -> None:
        """Initializes the device controller object."""
        self.sensors = sensors
        self.actuators = actuators

    def read_sensor(self, measurement: Measurement) -> list[Reading]:
        """Reads sensors with measurement type matching the provided measurement.

        Args:
          measurement (Measurement): the measurement to select sensors from.

        Returns:
            Readings from all sensors with the matching measurement type.
        """
        return [s.read_sensor() for s in self.sensors if s.measurement == measurement]

    def read_sensors(self) -> list[Reading]:
        """Reads all sensors.

        Returns:
            Readings from all sensors collected in a list.
        """
        return [s.read_sensor() for s in self.sensors]

    def control_actuator(self, command: Command) -> bool:
        """Runs the provided command on actuators that have a matching command type.

        Args:
          command (Command): the command to be passed to the actuators

        Returns:
            True if the state of an actuator changed as a result of applying the command.
            False if the state of an actuator did not change as a result of applying the command.
        """
        for actuator in self.actuators:
            if command.action == actuator.action:
                return actuator.control_actuator(command)
        return False
