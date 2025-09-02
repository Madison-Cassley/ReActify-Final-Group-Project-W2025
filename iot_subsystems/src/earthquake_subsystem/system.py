import asyncio
import logging

from common.devices.actuator import Action, Command
from common.devices.device_controller import DeviceController
from common.devices.sensor import Measurement
from common.interfaces import Interface

logger = logging.getLogger(__name__)


class System:
    def __init__(self, device_controller: DeviceController, interface: Interface, iot_device_client) -> None:
        self.device_controller = device_controller
        self.interface = interface
        self.iot_device_client = iot_device_client
        self.is_collecting_readings = True
        self.sleep_time = 2

        self.holding_f1 = False
        self.holding_f2 = False
        self.holding_f3 = False

    def process_command(self, command: Command) -> None:
        self.device_controller.control_actuator(command)

    def on_key_press(self, key: str) -> None:
        if key == "F1" and not self.holding_f1:
            self.holding_f1 = True
            logger.info("[F1] LED ON")
            self.process_command(Command(Action.LED_TOGGLE, data=1.0))

        elif key == "F2":
            self.holding_f2 = True

        elif key == "F3":
            self.holding_f3 = True

    def on_key_release(self, key: str) -> None:
        if key == "F1":
            self.holding_f1 = False
            logger.info("[F1] LED OFF")
            for actuator in self.device_controller.actuators:
                if hasattr(actuator, "turn_off"):
                    actuator.turn_off()

        elif key == "F2":
            self.holding_f2 = False

        elif key == "F3":
            self.holding_f3 = False

    async def collect_readings(self) -> None:
        while self.is_collecting_readings:
            if self.holding_f2:
                sound_reading = self.device_controller.read_sensor(Measurement.SOUND)
                val = sound_reading[0].value if isinstance(sound_reading, list) else sound_reading.value
                logger.info(f"[F2] Sound: {val}")

            if self.holding_f3:
                motion_reading = self.device_controller.read_sensor(Measurement.MOTION)
                val = motion_reading[0].value if isinstance(motion_reading, list) else motion_reading.value
                motion_status = "Motion Detected" if val == 1.0 else "No Motion"
                logger.info(f"[F3] Motion: {motion_status}")

            if self.iot_device_client:
                await self.iot_device_client.send_readings(self.device_controller.read_sensors())

            await asyncio.sleep(self.iot_device_client.get_interval())

    async def loop(self) -> None:
        self.interface.register_callback("on_press", self.on_key_press)
        self.interface.register_callback("on_release", self.on_key_release)

        async with asyncio.TaskGroup() as tg:
            tg.create_task(self.interface.event_loop())
            tg.create_task(self.collect_readings())
