import asyncio
import logging
from common.devices.actuator import Command
from common.devices.device_controller import DeviceController
from src.fire_air_quality_system.interfaces import Interface

from common.devices.sensor import Measurement
from common.iot import IOTDeviceClient

logger = logging.getLogger(__name__)

DEFAULT_SLEEP = 2

class System:
    """Class defining the connected object system.

    Attributes:
        device_controller (DeviceController): the system device controller
        interface (Interface): the system interface
    """
    device_controller: DeviceController
    interface: Interface
    iot_device_client: IOTDeviceClient
    is_collecting_readings: bool = True
    sleep_time: float = 2

    def __init__(self, device_controller: DeviceController, interface: Interface, iot_device_client: IOTDeviceClient) -> None:
        """Initializes the system."""
        self.device_controller = device_controller
        self.interface = interface
        self.iot_device_client = iot_device_client


    def process_command(self, command: Command) -> None:
        """Process a command using the device controller.

        Args:
          command (Command): the command to process.
        """
        self.device_controller.control_actuator(command)
 
    async def collect_readings(self) -> None:
        """Collect readings from device controller."""
        while self.is_collecting_readings:                
            logger.info(f"Sleeping for {self.sleep_time}...")               
            readings = self.device_controller.read_sensors()
            co2_level = self.device_controller.read_sensor(measurement= Measurement.CO2LEVEL)            
            co2_unit = Measurement.CO2LEVEL["unit"]            
            co2_sensor_format = f"{co2_level} {co2_unit}"
            logger.info(co2_sensor_format)               
            await self.iot_device_client.send_readings(readings)
            await asyncio.sleep(self.iot_device_client.get_interval())

    async def loop(self) -> None:
        """Initialize and close the interface loop and all other background tasks."""
        self.interface.register_callback("control_actuator", self.process_command)
        # TODO: add another task that uses the collect_readings method above.
        # See https://docs.python.org/3/library/asyncio-task.html#task-groups
        async with asyncio.TaskGroup() as tg:
            tg.create_task(self.interface.event_loop())
            tg.create_task(self.collect_readings())

