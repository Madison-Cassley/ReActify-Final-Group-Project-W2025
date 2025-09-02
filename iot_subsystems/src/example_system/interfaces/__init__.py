# File: src/example_system/interfaces/__init__.py
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

from common.devices.actuator import Action, Command
from common.interfaces import Interface
from common.interfaces.keyboard import KeyboardInterface
from common.interfaces.reterminal import ReterminalInterface

logger = logging.getLogger(__name__)


class ExampleSystemInterface(Interface):
    """Common logic for all example_system interfaces."""

    def key_press(self, key: str) -> None:
        """See base class."""
        if key.upper() == "F1":
            command = Command(Action.FAN_TOGGLE, 1)
            self.callbacks["control_actuator"](command)
        elif key.upper() == "O":
            logger.info("'O' pressed, script will exit when released")
        else:
            logger.debug(f"{key} pressed")

    def key_release(self, key: str) -> None:
        """See base class."""
        if key.upper() == "F1":
            command = Command(Action.FAN_TOGGLE, 0)
            self.callbacks["control_actuator"](command)
        elif key.upper() == "O":
            logger.info("'O' released, script exiting.")
            self.callbacks["end_event_loop"]()
        else:
            logger.debug(f"{key} released")


class ExampleSystemReterminalInterface(ExampleSystemInterface, ReterminalInterface):
    """Reterminal button-listener interface for the example_system reterminal."""


class ExampleSystemKeyboardInterface(ExampleSystemInterface, KeyboardInterface):
    """Keyboard button-listener interface for the example_system in development."""
