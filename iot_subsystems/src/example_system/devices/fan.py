# File: src/example_system/devices/fan.py
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
from time import sleep

from gpiozero import OutputDevice

from common.devices.actuator import Action, Command
from example_system.devices.toggle_actuator import ToggleActuator


class FanActuator(ToggleActuator):
    """Implementation of ToggleActuator with defaults specific to fans."""

    device: OutputDevice
    action: Action
    state: float = 0

    def __init__(self, device: OutputDevice) -> None:
        """FanActuator constructor."""
        self.device = device
        self.action = Action.FAN_TOGGLE


TEST_SLEEP_TIME = 1


def main() -> None:
    """Routine for testing fan when this file is run as a script rather than a module.
    Useful pattern when you want to test a single device in isolation.

    Usage:
        $ PYTHONPATH=src:${PYTHONPATH} python src/example_system/devices/aht20.py
    Alternatively:
        $ export PYTHONPATH=${HOME}/path-to-repository/src:${PYTHONPATH}
        $ python src/example_system/devices/aht20.py
    """
    fan = OutputDevice(pin=16)
    fan_actuator = FanActuator(device=fan)

    fan_on = Command(Action.FAN_TOGGLE, 1)
    fan_off = Command(Action.FAN_TOGGLE, 0)
    fan_actuator.control_actuator(fan_on)
    sleep(TEST_SLEEP_TIME)
    fan_actuator.control_actuator(fan_on)
    sleep(TEST_SLEEP_TIME)
    fan_actuator.control_actuator(fan_off)
    sleep(TEST_SLEEP_TIME)
    fan_actuator.control_actuator(fan_off)
    sleep(TEST_SLEEP_TIME)


if __name__ == "__main__":
    with contextlib.suppress(KeyboardInterrupt):
        main()
