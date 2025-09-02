from gpiozero import OutputDevice
from time import sleep
from dataclasses import dataclass
from common.devices.actuator import Action, Command, Actuator
import logging

logger = logging.getLogger(__name__)

@dataclass
class FanActuator(Actuator):
    """Actuator to control the state of a digital gpio fan"""
    device: OutputDevice
    action: Action
    state: float = 0

    def control_actuator(self, command: Command) -> bool:
        """Function that controls the fan actuator"""
        print("control_actuator called")  

        if (command.data == self.state):
            print("Is already on or off")
            print("Device value: ", self.device.value)
            logger.info(f"{self.action.name}: DEVICE ALREADY ON OR OFF") 
            self.device.value = command.data
            return False
        else: 
            self.state = command.data
            self.action = command.action          
            self.device.toggle()  
            print("Fan value after toggle: ", self.device.value) 
            logger.info(f"{self.action.name}: DEVICE TOGGLED")                
            return True

    
TEST_SLEEP_TIME = 5


def main():
    """Routine for testing actuators when this file is run as a script rather than a module."""
    fan = OutputDevice(pin=16, active_high=True)
    fan_actuator = FanActuator(device=fan, action=Action.FAN_TOGGLE)

    while True:
        fan_on = Command(Action.FAN_TOGGLE, 1)
        fan_off = Command(Action.FAN_TOGGLE, 0)
        fan_actuator.control_actuator(fan_on)
        sleep(TEST_SLEEP_TIME)
        fan_actuator.control_actuator(fan_on)
        sleep(TEST_SLEEP_TIME)
        fan_actuator.control_actuator(fan_off)
        sleep(TEST_SLEEP_TIME)
        fan_actuator.control_actuator(fan_off)
        sleep(TEST_SLEEP_TIME)

if __name__ == "__main__":
    """
    Usage:
        $ PYTHONPATH=${PYTHONPATH}:src python src/Alex_system/devices/fan.py
    Alternatively:
        $ export PYTHONPATH=${PYTHONPATH}:${HOME}/path-to-repository/src
        $ python src/Alex_system/devices/fan.py
    """
    try:        
        main()
    except KeyboardInterrupt:
        pass