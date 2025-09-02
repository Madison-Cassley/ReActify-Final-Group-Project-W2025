# File: tests/example_system/integration/conftest.py
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

from common.devices.sensor import Reading
from example_system.interfaces import ExampleSystemInterface
from example_system.iot.azure_device_client import AzureDeviceClient


class MockInterface(ExampleSystemInterface):
    async def mock_event(self) -> dict:
        return {}

    async def event_loop(self) -> None:
        event = await self.mock_event()
        if event.get("value") == 1:
            self.key_press(event["key"])
        elif event.get("value") == 0:
            self.key_release(event["key"])

    def end_event_loop(self) -> None:
        pass

    def key_press(self, key: str) -> None:
        return super().key_press(key)

    def key_release(self, key: str) -> None:
        return super().key_release(key)


class MockIOTDeviceClient(AzureDeviceClient):
    async def connect(self) -> None:
        pass

    async def send_reading(self, reading: Reading) -> None:
        pass
