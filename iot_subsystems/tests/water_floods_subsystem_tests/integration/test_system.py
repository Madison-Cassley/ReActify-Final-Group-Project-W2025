# File: tests/example_system/integration/test_system.py
# Project: final-project-upstream
# Creation date: 29 Apr 2025
# Author: michaelhaaf <michael.haaf@gmail.com>
# Modified By: Madison Cassley
# Changes made: modified imports to work with my system and adjusted the code to my system
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

from src.water_floods_subsystem.interfaces.system_interface import WaterFloodsSystem

os.environ["ENVIRONMENT"] = "DEVELOPMENT"
os.environ["IOTHUB_CONNECTION_STRING"] = "HostName=fake;DeviceId=fake;SharedAccessKey=fake"

def test_system_initializes_and_reads_sensors():
    system = WaterFloodsSystem()
    readings = system.device_controller.read_sensors()
    assert len(readings) == 2
    for r in readings:
        assert hasattr(r, "value")
        assert hasattr(r, "measurement")