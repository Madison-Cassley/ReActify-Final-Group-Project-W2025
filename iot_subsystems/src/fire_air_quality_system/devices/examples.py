# TODO: delete this file once you have updated conftest.py, see April 11 instructrions.

from dataclasses import dataclass
from grove.grove_temperature_humidity_aht20 import GroveTemperatureHumidityAHT20

from gpiozero import OutputDevice, PWMLED
from dataclasses import dataclass
from common.devices.actuator import Action, Command, Actuator
from common.devices.sensor import Sensor, Measurement, Reading

@dataclass
class TemperatureSensor(Sensor):
    """Implementation of Sensor for taking Temperature measurements."""

    device: GroveTemperatureHumidityAHT20
    measurement: Measurement

    # TODO: complete this function
    def read_sensor(self) -> Reading:
        """See base class."""
        pass

@dataclass
class HumiditySensor(Sensor):
    """Implementation of Sensor class for taking Humidity measurements."""

    device: GroveTemperatureHumidityAHT20
    measurement: Measurement

    # TODO: complete this function
    def read_sensor(self) -> Reading:
        """See base class."""
        pass

@dataclass
class LEDToggleActuator(Actuator):
    """Implementation of Actuator for toggling an LED."""

    device: OutputDevice
    action: Action
    state: float

    def control_actuator(self, command: Command) -> bool:
        """See base class."""
        pass


@dataclass
class LEDPulseActuator(Actuator):
    """Implementation of Actuator for pulsing an LED."""

    device: PWMLED
    action: Action
    state: float

    def control_actuator(self, command: Command) -> bool:
        """See base class."""
        pass


@dataclass
class LEDBrightnessActuator(Actuator):
    """Implementation of Actuator for changing the brightness of an LED using PWM."""

    device: PWMLED
    action: Action
    state: float

    def control_actuator(self, command: Command) -> bool:
        """See base class."""
        pass
