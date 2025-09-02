from abc import ABC, abstractmethod
from typing import Callable
from common.iot.azure_device_client import AzureDeviceClient
from common.devices.actuator import Action, Command


class Interface(ABC):
    """Abstract class defining common interface methods for the system.

    Attributes:
        callbacks (dict[str, Callable]): dictionary of key->callback pairs.
    """

    callbacks: dict[str, Callable]

    def __init__(self) -> None:
        """Initizalizes the system interface."""
        self.callbacks = {
            "control_actuator": lambda: print("Interface callback 'control_actuator' not implemented")
        }

    @abstractmethod
    async def event_loop(self) -> None:
        """Runs an event loop that listens for interface actions.

        Blocks the thread during the execution of the loop.
        """
        pass

    @abstractmethod
    def end_event_loop(self) -> None:
        """Terminates the event loop started by the event_loop method."""
        pass

    def register_callback(self, key: str, callback: Callable) -> None:
        """Connects the system interface to the system using a callback pattern.

        Args:
            key (str): the key to reference a given callback function
            callback (Callable): the callback to be used by the interface for the given key
        """
        self.callbacks[key] = callback

    def key_press(self, key: str) -> None:
        """Defines the default behavior when particular keys in the interface are pressed.

        Args:
          key (str): the string defining the key that has been pressed.
        """
        if key.upper() == "F1":
            print("F1 pressed!")
            command = Command(Action.FAN_TOGGLE, 1)            
            self.callbacks["control_actuator"](command)
        elif key.upper() == "F2":
            print("F2 pressed!")
            command = Command(Action.RGB_LED_TOGGLE, 1)           
            self.callbacks["control_actuator"](command) 
        elif key.upper() == "F3":
            print("F3 pressed!")                   
            command = Command(Action.RGB_LED_RED, 1)           
            self.callbacks["control_actuator"](command)  
        elif key.upper() == "O":
            print("'O' pressed, script will exit when released")

    def key_release(self, key: str) -> None:
        """Defines the default behavior when particular keys in the interface are pressed.

        Args:
          key (str): the string defining the key that has been pressed.
        """
        if key.upper() == "F1":
            print("F1 released!")
            command = Command(Action.FAN_TOGGLE, 0)
            self.callbacks["control_actuator"](command)        
        elif key.upper() == "F2":
            print("F2 released!")
            command = Command(Action.RGB_LED_TOGGLE, 0)           
            self.callbacks["control_actuator"](command)   
        # TODO: Implement this to turn off the LED
        elif key.upper() == "F3":
            print("F3 released!")
            command = Command(Action.RGB_LED_RED, 0)           
            self.callbacks["control_actuator"](command)  
        elif key.upper() == "O":
            print("'O' released, script will exit.")
            self.end_event_loop()
