# File: src/example_system/devices/toggle_actuator.py
# Project: final-project-upstream
# Creation date: 29 Apr 2025
# Author: michaelhaaf <michael.haaf@gmail.com>
# Modified By: Madison Cassley
# Changes made: Added my own actuator for my buzzer
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

logger = logging.getLogger(__name__)

class ToggleActuator(Actuator):
    def control_actuator(self, command: Command) -> bool:
        if command.action is not self.action:
            logger.warning(f"ToggleActuator got wrong action: {command.action}")
            return False
        if not (self.action.min_value <= command.data <= self.action.max_value):
            logger.error(f"{self.action.name} data {command.data} out of bounds")
            return False
        if command.data == self.state:
            return False

        #apply change
        self.device.value = bool(command.data)
        self.state = command.data
        state_str = "ON" if self.state else "OFF"
        logger.info(f"{self.action.name} → {state_str}")
        return True
