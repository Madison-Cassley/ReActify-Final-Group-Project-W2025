# File: src/example_system/runner.py
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
import contextlib
import logging
import sys
import logging

from dotenv import dotenv_values
from gpiozero import OutputDevice
from gpiozero.pins.mock import MockFactory

from common.devices.device_controller import DeviceController
from example_system.devices.aht20 import (
    HumiditySensor,
    MockGroveTemperatureHumidityAHT20,
    TemperatureSensor,
)
from example_system.devices.fan import FanActuator
from example_system.example_system import ExampleSystem
from example_system.interfaces import (
    ExampleSystemKeyboardInterface,
    ExampleSystemReterminalInterface,
)
from common.iot.azure_device_client import AzureDeviceClient


logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter(
    "%(asctime)s %(name)s %(levelname)s: %(message)s"
)

#STDOUT handler
sh = logging.StreamHandler(sys.stdout)
sh.setFormatter(formatter)
logger.addHandler(sh)

#file handler
fh = logging.FileHandler("system.log")
fh.setFormatter(formatter)
logger.addHandler(fh)

# https://www.gnu.org/licenses/gpl-3.0.html#howto
LICENSE_NOTICE = """
example_system: Copyright (C) 2025 michaelhaaf
This program comes with ABSOLUTELY NO WARRANTY.
This is free software, and you are welcome to redistribute it
under certain conditions; for details see LICENSE packaged with source code.
"""


def main() -> None:
    """Routine for running system from cli."""
    runtime_environment = "DEVELOPMENT"
    if runtime_environment == "DEVELOPMENT":
        interface = ExampleSystemKeyboardInterface()
        aht20 = MockGroveTemperatureHumidityAHT20()
        fan = OutputDevice(pin=16, pin_factory=MockFactory())
    elif runtime_environment == "PRODUCTION":
        interface = ExampleSystemReterminalInterface()
        aht20 = GroveTemperatureHumidityAHT20(address=0x38, bus=4)
        fan = OutputDevice(pin=16)
    else:
        raise ValueError

    sensors = [TemperatureSensor(device=aht20), HumiditySensor(device=aht20)]
    actuators = [FanActuator(device=fan)]

    device_controller = DeviceController(sensors=sensors, actuators=actuators)
    system = ExampleSystem(
        device_controller=device_controller,
        interface=interface,
        iot_device_client=AzureDeviceClient(),
    )

    try:
        print(LICENSE_NOTICE)
        asyncio.run(system.loop())
    except StopAsyncIteration as e:
        logger.error(e)  # noqa: TRY400


if __name__ == "__main__":
    with contextlib.suppress(KeyboardInterrupt):
        main()
