# File: src/example_system/example_system.py
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

import asyncio
import logging

from common.devices.actuator import Command
from common.devices.device_controller import DeviceController
from common.interfaces import Interface
from common.iot import IOTDeviceClient

logger = logging.getLogger(__name__)


class ExampleSystem:
    """Class defining the connected object system.

    Attributes:
        device_controller (DeviceController): the system device controller
        interface (Interface): the interface listening for button presses on the device
        iot_device_client (Interface): the client for communicating with an IoT Hub
    """

    device_controller: DeviceController
    interface: Interface
    iot_device_client: IOTDeviceClient

    is_collecting_readings: bool = True
    telemetry_interval: float = 5
    loop_stop = asyncio.Event()

    def __init__(
        self,
        device_controller: DeviceController,
        interface: Interface,
        iot_device_client: IOTDeviceClient,
    ) -> None:
        """Initializes the system."""
        self.device_controller = device_controller
        self.interface = interface
        self.iot_device_client = iot_device_client

    def process_command(self, command: Command) -> bool:
        """Process a command.

        Args:
          command (Command): the command to process.
        """
        return self.device_controller.control_actuator(command)

    async def keep_loop_alive_until_cancelled(self) -> None:
        """Keeps event loop running until requested by an interface callback."""
        await self.loop_stop.wait()
        raise asyncio.CancelledError

    def end_loop(self) -> None:
        """Ends loop."""
        self.loop_stop.set()

    async def collect_readings(self) -> None:
        """Collect readings."""
        while self.is_collecting_readings:
            readings = self.device_controller.read_sensors()
            await self.iot_device_client.send_readings(readings)
            await asyncio.sleep(self.telemetry_interval)

    async def loop(self) -> None:
        """Initialize and close the interface loop."""
        self.interface.register_callback("control_actuator", self.process_command)
        self.interface.register_callback("end_event_loop", self.end_loop)
        try:
            async with asyncio.TaskGroup() as tg:
                tg.create_task(self.collect_readings())
                tg.create_task(self.interface.event_loop())
                await self.keep_loop_alive_until_cancelled()
        except asyncio.CancelledError:
            logger.info("Script exiting.")
