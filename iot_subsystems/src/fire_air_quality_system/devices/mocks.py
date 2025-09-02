from random import random
import time
from dataclasses import dataclass
from grove.grove_temperature_humidity_aht20 import GroveTemperatureHumidityAHT20
from src.common.devices.sensor import Sensor, Measurement, Reading
from src.common.devices.actuator import Actuator, Action, Command
from src.common.devices.device_controller import DeviceController
from src.fire_air_quality_system.iot.azure_device_client import AzureDeviceClient
from src.fire_air_quality_system.devices.CO2Sensor import GroveVOCeCO2Sensor, CO2Sensor
import asyncio

 
class MockGroveTemperatureHumidityAHT20(GroveTemperatureHumidityAHT20):
    """Mock implementation of the GroveTemperatureHumidityAHT20."""

    def __init__(self, address: int = 0x38, bus: int = 4) -> None:
        """Initializes the mock class."""
        self.address = address
        self.bus = bus

    def read(self) -> tuple[float, float]:
        """Returns a random reading between 0-100 for temperature and humidity."""
        return (random() * 100, random() * 100)
        
    def read_temperature(self):
        """Returns a random reading between 0-100 for temperature and humidity."""
        return (random() * 100)
    
    def read_humidity(self):
        """Returns a random reading between 0-100 for temperature and humidity."""
        return (random() * 100)


class MockGroveVOCeCO2Sensor(GroveVOCeCO2Sensor):
    
    def __init__(self, address: int = 0x38, bus: int = 4) -> None:
        """Initializes the mock class."""
        self.address = address
        self.bus = bus

    def read_CO2_level(self) -> tuple[float, float]:
        """Returns a random reading between 0-2100 for for CO2 level."""        
        return random() * 2100

class MockNeoPixel:
    def __init__(self, pin, num_pixels, auto_write=True):
        self.n = num_pixels
        self.pixels = [(0, 0, 0)] * num_pixels
        self.auto_write = auto_write

    def __setitem__(self, index, color):
        self.pixels[index] = color
        if self.auto_write:
            self.show()

    def __getitem__(self, index):
        return self.pixels[index]

    def fill(self, color):
        self.pixels = [color] * self.n
        if self.auto_write:
            self.show()

    def show(self):
        print(f"MockNeoPixel showing: {self.pixels}")

    def deinit(self):
        self.fill((0, 0, 0))
        print("MockNeoPixel deinitialized")

@dataclass
class MockRBGLedStickActuator(Actuator):
    """Actuator to control the state of a digital gpio LED"""    
    action: Action
    state: float = 0
    device : float = 0

    def control_actuator(self, command: Command) -> bool:
        """Function that controls the RGB Led actuator"""
       
        if (command.data == self.state):
            print("Is already on or off")
            return False
        else:
            if (command.action == Action.RGB_LED_TOGGLE):
                self.state = command.data
                self.action = command.action
                self.device = command.data                              
            elif (command.action == Action.RGB_LED_RED):
                self.state = command.data
                self.action = command.action
                self.device = command.data  
            return True

@dataclass
class MockAzureDeviceClient():
    
    devices: DeviceController
    
    def __init__(self, device_controllers):
        self.devices = device_controllers                 


    def connect(self) -> None:
        print("Connected")

       
    def send_reading(self, reading: Reading) -> None:
        print(reading)   

    def send_readings(self, readings: list[Reading]) -> None:
        print(readings)  


async def main():
    sensor = MockGroveVOCeCO2Sensor()
    CO2Level = CO2Sensor(sensor, Measurement.CO2LEVEL)
    iot_device_client = AzureDeviceClient([])
    
    while True:       
        co2Reading= CO2Level.read_sensor()
        await iot_device_client.send_reading(co2Reading)
        
        #print(co2Reading) 
        time.sleep(5)


if __name__ == "__main__":
    """
    Usage:
        $ PYTHONPATH=${PYTHONPATH}:src python src/Alex_system/devices/mocks.py
    Alternatively:
        $ export PYTHONPATH=${PYTHONPATH}:${HOME}/path-to-repository/src
        $ python src/Alex_system/devices/mocks.py
    """

    # Surrounding the main() method in a try/except block allows us to use Ctrl+c to exit the script execution gracefully
    try:        
         asyncio.run(main())
    except KeyboardInterrupt:
        pass