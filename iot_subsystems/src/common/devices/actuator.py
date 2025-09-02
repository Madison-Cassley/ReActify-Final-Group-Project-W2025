# File: src/common/devices/actuator.py
# Project: final-project-upstream
# Creation date: 29 Apr 2025
# Author: michaelhaaf <michael.haaf@gmail.com>
# Modified By: Madison Cassley
# Changes made: added more actuators to the enum
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


class Action(dict, Enum):
    """Enum defining valid command actions and valid value ranges.

    Supports JSON serialization by overriding dict.

    Used by the Command and Actuator classes to distinguish commands and target actuators.

    Attributes:
        description (str): string describing the purpose and target device of the command action
        min_value (float): float defining the minimum valid value for this command
        max_value (float): float defining the maximum valid value for this command
        name (str): String that is the unique name of the action.
    """

    FAN_TOGGLE = {
        "min_value": 0,
        "max_value": 1,
        "description": "Command to turn the fan on/off",
    }

    LED_TOGGLE = {
        "min_value": 0,
        "max_value": 1,
        "description": "Command to turn the LED on/off",
    }

    # LED_PULSE = {
    #     "min_value": 0.0,
    #     "max_value": 1800.0,
    #     "description": "Command to pulse the LED for a specified duration",
    # }

    # LED_BRIGHTNESS = {
    #     "min_value": 0.0,
    #     "max_value": 1.0,
    #     "description": "Command to set the brightness of the LED",
    # }
    
    RGB_LED_TOGGLE = {
        "min_value": 0,
        "max_value": 1,
        "description": "Command to turn the RGB Led on/off"
    }

    RGB_LED_RED = {
        "min_value": 0,
        "max_value": 1,
        "description": "Command to set the light RED"
    }

    RGB_LED_YELLOW = {
        "min_value": 0,
        "max_value": 1,
        "description": "Command to set the light YELLOW"
    }

    RGB_LED_GREEN = {
        "min_value": 0,
        "max_value": 1,
        "description": "Command to set the light GREEN"
    }


    SERVO_ANGLE = {
        "min_value": 0.0, 
        "max_value": 180,
        "description": "Command to set servo angle in °"
    }

    BUZZER_TOGGLE = {
        "min_value": 0,   
        "max_value": 1,   
        "description": "Command to toggle buzzer on/off"
    }

    def __init__(self, items: dict) -> None:
        """Initialize the Action instance.

        Args:
            items (dict[str]): the dictionary to initialize the Measurement from.
                                Note: requires "unit" and "description" keys.
        """
        self.description = items["description"]
        self.min_value = items["min_value"]
        self.max_value = items["max_value"]
        super().__init__({"name": self.name} | items)


@dataclass
class Command:
    """Class for creating actuator commands.

    Attributes:
        action (Action): an action that the command triggers
        data (float): the data associated with this command, used to set the actuator state
    """

    action: Action
    data: float


class Actuator(ABC):
    """Abstract class providing a common interface to GPIO actuators.

    Attributes:
        device (Any): the external module used to control the actuator
        action (Action): the action that determines the types of commands that the actuator can process
        state (float): the current state of the actuator
    """

    device: Any
    action: Action
    state: float

    @abstractmethod
    def control_actuator(self, command: Command) -> bool:
        """Process a provided command.

        Checks if the command's action type matches the actuator's action. If so, uses the internal
        device object to apply the action in the real world and updates the state of the actuator.

        Uses the action attribute to ensure the command data is within a valid range.

        Args:
          command (Command): the command to process.

        Returns:
            True if the state of the actuator changed as a result of applying the command.
            False if the state of the actuator did not change as a result of processing the command.
        """
        pass
