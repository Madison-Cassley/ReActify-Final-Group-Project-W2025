import asyncio
import contextlib
import logging
import os
import sys

from dotenv import load_dotenv

from common.devices.device_controller import DeviceController
from earthquake_subsystem.interfaces.system_interface import KeyboardInterface, ReterminalInterface
from common.iot.azure_device_client import AzureDeviceClient
from earthquake_subsystem.system import System


def main() -> None:
    load_dotenv()

    LOG_FILE = "system.log"
    logging.basicConfig(
        level=logging.INFO,
        format="%(message)s",
        handlers=[logging.StreamHandler(sys.stdout), logging.FileHandler(LOG_FILE, mode="a")],
    )

    # Hiding detailed Azure IoT SDK logs, like:
    # "Creating client for connecting using MQTT over TCP"
    # "Connect using port 8883 (TCP)", and other internal connection messages
    logging.getLogger("azure").setLevel(logging.WARNING)

    env = os.getenv("ENVIRONMENT", "DEVELOPMENT")

    if env == "PRODUCTION":
        from earthquake_subsystem.devices.led_stick import LEDStickActuator
        from earthquake_subsystem.devices.pir_sensor import PIRSensor
        from earthquake_subsystem.devices.sound_sensor import SoundSensor
    else:
        from earthquake_subsystem.devices.mock_led_stick import MockLEDStickActuator as LEDStickActuator
        from earthquake_subsystem.devices.mock_pir_sensor import MockPIRSensor as PIRSensor
        from earthquake_subsystem.devices.mock_sound_sensor import MockSoundSensor as SoundSensor

    sensors = [PIRSensor(), SoundSensor()]
    actuators = [LEDStickActuator()]

    interface = ReterminalInterface() if env == "PRODUCTION" else KeyboardInterface()
    device_controller = DeviceController(sensors=sensors, actuators=actuators)
    azure_client = AzureDeviceClient(device_controller)

    async def run():
        await azure_client.connect()
        system = System(
            device_controller=device_controller, interface=interface, iot_device_client=azure_client
        )
        await system.loop()

    try:
        asyncio.run(run())
    except StopAsyncIteration:
        pass


if __name__ == "__main__":
    with contextlib.suppress(KeyboardInterrupt):
        main()
