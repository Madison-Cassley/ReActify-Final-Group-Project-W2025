import asyncio
import contextlib
import os
import asyncio
import neopixel
import board   
from gpiozero import OutputDevice, PWMLED, LED
from gpiozero.pins.mock import MockFactory
from fire_air_quality_system.devices.mocks import MockGroveVOCeCO2Sensor, MockNeoPixel, MockRBGLedStickActuator
from fire_air_quality_system.devices.CO2Sensor import CO2Sensor, GroveVOCeCO2Sensor
#from iot.azure_device_client import AzureDeviceClient
from common.iot.azure_device_client import AzureDeviceClient
from common.devices.actuator import Action
from common.devices.sensor import Measurement
from common.devices.device_controller import DeviceController
from devices.fan import FanActuator
from devices.RGBLedStick import RBGLedStickActuator
# from interfaces.reterminal import ReterminalInterface
# from interfaces.keyboard import KeyboardInterface
from interfaces.system_interface import ReterminalInterface, KeyboardInterface



from system import System

#Permits access to specific .env file and its content
from dotenv import load_dotenv
load_dotenv() # load env file into enviroment variables


def main() -> None:
    """Routine for running system from cli."""
  
   
    

    runtime_environment = os.getenv("RUNTIME_ENVIRONMENT")  
    print(runtime_environment)  
    if runtime_environment == "DEVELOPMENT":   
        mockCO2Sensor = MockGroveVOCeCO2Sensor()      
        ledDeviceMock = LED(pin=12, pin_factory=MockFactory())       
        interface = KeyboardInterface()
        sensors = [
            CO2Sensor(mockCO2Sensor, Measurement.CO2LEVEL)
        ]
        actuators = [            
            FanActuator(device=OutputDevice(pin=16, pin_factory=MockFactory()),action=Action.FAN_TOGGLE),
            MockRBGLedStickActuator(action=Action.RGB_LED_TOGGLE),  
            MockRBGLedStickActuator(action=Action.RGB_LED_RED),                   
        ]
    elif runtime_environment == "PRODUCTION":       
        try:  
            co2sensor = GroveVOCeCO2Sensor()         
            pixels = neopixel.NeoPixel(board.D18, 10, auto_write=False) 
        except:
            print("WARNING: Cannot instantiate PWMLED on Production mode if using WSL. Please switch runtime environment to Development")
            pass

        interface = ReterminalInterface()
        sensors = [
            CO2Sensor(co2sensor, Measurement.CO2LEVEL)
        ]
        actuators = [            
            FanActuator(device=OutputDevice(pin=16), action=Action.FAN_TOGGLE),   
            RBGLedStickActuator(device=pixels, action=Action.RGB_LED_TOGGLE), 
            RBGLedStickActuator(device=pixels, action=Action.RGB_LED_RED),
            RBGLedStickActuator(device=pixels, action=Action.RGB_LED_YELLOW),
            RBGLedStickActuator(device=pixels, action=Action.RGB_LED_GREEN)             
        ]
    else:
        raise ValueError
   
    device_controller = DeviceController(sensors=sensors, actuators=actuators)
    #iot_device_client = AzureDeviceClient(device_controller)
    iot_device_client = AzureDeviceClient(device_controller)
    asyncio.run(iot_device_client.connect())
    
    
    system = System(device_controller=device_controller, interface=interface, iot_device_client= iot_device_client)

    try:
        asyncio.run(system.loop())
    except StopAsyncIteration as e:
        print(e)


if __name__ == "__main__":
    with contextlib.suppress(KeyboardInterrupt):
        main()


# Notes: Due to RGB Led stick requiring root permissions to execute, run the following command:
# sudo PYTHONPATH=${PYTHONPATH}:src ~/Documents/repositories/final-project-refarminal/iot_subsystems/.venv/bin/python src/Alex_system

