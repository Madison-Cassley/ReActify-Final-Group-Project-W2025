import json
import logging
import os
import asyncio

from azure.iot.device import Message
from azure.iot.device.aio import IoTHubDeviceClient
from dotenv import load_dotenv

from common.devices.sensor import Reading
from common.iot import IOTDeviceClient

logger = logging.getLogger(__name__)


class AzureDeviceClient(IOTDeviceClient):
    """IOT integrations with Azure IoT Hub."""

    def __init__(self):
        load_dotenv()
        self.conn_str = os.getenv("IOT_DEVICE_CONNECTION_STRING")
        if not self.conn_str:
            raise ValueError("Missing IOT_DEVICE_CONNECTION_STRING in .env")
        self.client = IoTHubDeviceClient.create_from_connection_string(self.conn_str)

    async def connect(self) -> None:
        logger.info("[AZURE] Connecting to Azure IoT Hub...")
        await self.client.connect()

    async def send_reading(self, reading: Reading) -> None:
        msg = Message(json.dumps({"value": reading.value, "measurement": reading.measurement.name}))
        msg.custom_properties["measurement"] = reading.measurement.name
        logger.info(f"[AZURE] Sending single reading: {msg}")
        await self.client.send_message(msg)

    async def send_readings(self, readings: list[Reading]) -> None:
        for r in readings:
            await self.send_reading(r)
            await asyncio.sleep(1.5)
