# File: src/example_system/iot/azure_device_client.py
# Project: final-project-upstream
# Creation date: 29 Apr 2025
# Author: michaelhaaf <michael.haaf@gmail.com>
# Modified By: Madison Cassley
# Changes made: Made it work with my own IoT
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

# src/water_floods_subsystem/iot/azure_device_client.py

import os, json, logging
from azure.iot.device import Message, MethodResponse
from azure.iot.device.aio import IoTHubDeviceClient
from common.devices.sensor import Reading

logger = logging.getLogger(__name__)

class AzureDeviceClient:
    def __init__(self):
        conn_str = os.getenv("IOTHUB_CONNECTION_STRING")
        if not conn_str:
            raise ValueError("IOTHUB_CONNECTION_STRING not set in .env")
        self._conn_str = conn_str
        self._client: IoTHubDeviceClient | None = None

    async def connect(self) -> None:
        self._client = IoTHubDeviceClient.create_from_connection_string(self._conn_str)
        await self._client.connect()
        logger.warning("✔ Connected to Azure IoT Hub")

    async def send_reading(self, reading: Reading) -> None:
        body = {"value": reading.value, "measurement": dict(reading.measurement)}
        msg = Message(json.dumps(body))
        msg.custom_properties["measurement"] = reading.measurement.name
        await self._client.send_message(msg)

    async def send_readings(self, readings: list[Reading]) -> None:
        for r in readings:
            await self.send_reading(r)

    async def handle_method_requests(self, device_controller) -> None:
        """
        Listen for direct-method calls and dispatch to actuators.
        Expects method names "SetServoAngle" & "ToggleBuzzer" with payload {"data":<int>}.
        """
        from common.devices.actuator import Command, Action

        while True:
            request = await self._client.receive_method_request()  # blocks until a method call
            payload = request.payload or {}
            status = 200
            resp_payload = {"status": "ok"}

            if request.name == "SetServoAngle":
                angle = payload.get("data", 0)
                success = device_controller.control_actuator(
                    Command(Action.SERVO_ANGLE, angle)
                )
                if not success:
                    status = 400
                    resp_payload = {"status": "servo failed"}
            elif request.name == "ToggleBuzzer":
                state = payload.get("data", 0)
                success = device_controller.control_actuator(
                    Command(Action.BUZZER_TOGGLE, state)
                )
                if not success:
                    status = 400
                    resp_payload = {"status": "buzzer failed"}
            else:
                status = 404
                resp_payload = {"status": "unknown method"}

            #send back method response
            response = MethodResponse.create_from_method_request(
                request, status=status, payload=resp_payload
            )
            await self._client.send_method_response(response)

