# File: src/example_system/devices/toggle_actuator.py
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

from gpiozero import OutputDevice

from common.devices.actuator import Action, Actuator, Command

logger = logging.getLogger(__name__)


class ToggleActuator(Actuator):
    """Implementation of Actuator that turns a device on/off.
    Can be used as a base class for many different devices (fan, LED, etc.)

    Attributes:
        device (type[OutputDevice]): a gpiozero module inheriting the OutputDevice class
        action (Action): see base class
        state (float): represents the state of the actuator (0 if the actuator is off, 1 if the actuator is on)
    """

    device: OutputDevice
    action: Action
    state: float = 0

    def control_actuator(self, command: Command) -> bool:
        """See base class."""
        if command.action != self.action:
            logger.info("INVALID COMMAND ACTION")
            return False

        new_state = int(command.data)
        if new_state == self.action.max_value:
            return self.__on()
        if new_state == self.action.min_value:
            return self.__off()
        logger.info("INVALID COMMAND DATA")
        return False

    def __off(self) -> bool:
        if self.device.value == 0:
            logger.info(f"{self.action.name}: DEVICE ALREADY OFF")
            return False
        logger.info(f"{self.action.name}: TURNING DEVICE OFF")
        self.device.off()
        self.state = 0
        return True

    def __on(self) -> bool:
        if self.device.value == 1:
            logger.info(f"{self.action.name}: DEVICE ALREADY ON")
            return False
        logger.info(f"{self.action.name}: TURNING DEVICE ON")
        self.device.on()
        self.state = 1
        return True
