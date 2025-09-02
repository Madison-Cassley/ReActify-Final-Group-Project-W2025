# File: tests/example_system/integration/test_system.py
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

import pytest
from asyncmock import AsyncMock
from logot import Logot, logged

from common.devices.device_controller import DeviceController
from example_system.devices.fan import FanActuator
from example_system.example_system import ExampleSystem
from example_system.interfaces import ExampleSystemInterface, Interface
from example_system.iot.azure_device_client import AzureDeviceClient

from .conftest import MockInterface, MockIOTDeviceClient


@pytest.fixture
def mock_interface() -> ExampleSystemInterface:
    return MockInterface()


@pytest.fixture
def mock_iot_device_client() -> AzureDeviceClient:
    return MockIOTDeviceClient()


@pytest.fixture
def system(
    device_controller: DeviceController,
    mock_interface: Interface,
    mock_iot_device_client: AzureDeviceClient,
) -> ExampleSystem:
    return ExampleSystem(device_controller, mock_interface, mock_iot_device_client)


@pytest.mark.asyncio
async def test_loop_all_sensor_readings_logged_with_correct_units(
    system: ExampleSystem, logot: Logot
):
    system.telemetry_interval = 0.1
    async with asyncio.TaskGroup() as tasks:
        test_task = tasks.create_task(system.loop())
        await logot.await_for(logged.info("%s%f%sRH%s"), timeout=0.2)
        await logot.await_for(logged.info("%s%f%s°C%s"), timeout=0.2)
        test_task.cancel()


@pytest.mark.asyncio
async def test_loop_f1_press_turns_fan_on(
    mocker, system: ExampleSystem, fan_actuator: FanActuator, logot: Logot
):
    mock_key_press = {"value": 1, "key": "F1"}
    mocker.patch.object(
        MockInterface, "mock_event", AsyncMock(return_value=mock_key_press)
    )
    fan_actuator.device.value = 0
    async with asyncio.TaskGroup() as tasks:
        test_task = tasks.create_task(system.loop())
        await logot.await_for(logged.info("%sFAN_TOGGLE%sON%s"))
        test_task.cancel()
    assert fan_actuator.device.value == 1


@pytest.mark.asyncio
async def test_loop_f1_release_turns_fan_off(
    mocker, system: ExampleSystem, fan_actuator: FanActuator, logot: Logot
):
    mock_key_release = {"value": 0, "key": "F1"}
    mocker.patch.object(
        MockInterface, "mock_event", AsyncMock(return_value=mock_key_release)
    )
    fan_actuator.device.value = 1
    async with asyncio.TaskGroup() as tasks:
        test_task = tasks.create_task(system.loop())
        await logot.await_for(logged.info("%sFAN_TOGGLE%sOFF%s"))
        test_task.cancel()
    assert fan_actuator.device.value == 0


@pytest.mark.asyncio
async def test_loop_f2_press_gets_logged(mocker, system: ExampleSystem, logot: Logot):
    mock_key_press = {"value": 1, "key": "F2"}
    mocker.patch.object(
        MockInterface, "mock_event", AsyncMock(return_value=mock_key_press)
    )
    async with asyncio.TaskGroup() as tasks:
        test_task = tasks.create_task(system.loop())
        await logot.await_for(logged.debug("F2 pressed"))
        test_task.cancel()


@pytest.mark.asyncio
async def test_loop_f2_release_gets_logged(mocker, system: ExampleSystem, logot: Logot):
    mock_key_release = {"value": 0, "key": "F2"}
    mocker.patch.object(
        MockInterface, "mock_event", AsyncMock(return_value=mock_key_release)
    )
    async with asyncio.TaskGroup() as tasks:
        test_task = tasks.create_task(system.loop())
        await logot.await_for(logged.debug("F2 released"))
        test_task.cancel()
