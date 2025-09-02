# File: tests/example_system/unit/test_fan.py
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

from common.devices.actuator import Action, Command
from example_system.devices.fan import FanActuator


def test_control_actuator_return_true_off_to_on(fan_actuator: FanActuator):
    fan_on = Command(Action.FAN_TOGGLE, 1)
    assert fan_actuator.control_actuator(fan_on)
    assert fan_actuator.device.value == 1


def test_control_actuator_return_true_on_to_off(fan_actuator: FanActuator):
    fan_on = Command(Action.FAN_TOGGLE, 1)
    fan_off = Command(Action.FAN_TOGGLE, 0)
    fan_actuator.control_actuator(fan_on)
    assert fan_actuator.control_actuator(fan_off)
    assert fan_actuator.device.value == 0


def test_control_actuator_return_false_on_to_on(fan_actuator: FanActuator):
    fan_on = Command(Action.FAN_TOGGLE, 1)
    fan_actuator.control_actuator(fan_on)
    assert not fan_actuator.control_actuator(fan_on)
    assert fan_actuator.device.value == 1


def test_control_actuator_return_false_off_to_off(fan_actuator: FanActuator):
    fan_off = Command(Action.FAN_TOGGLE, 0)
    fan_actuator.control_actuator(fan_off)
    assert not fan_actuator.control_actuator(fan_off)
    assert fan_actuator.device.value == 0
