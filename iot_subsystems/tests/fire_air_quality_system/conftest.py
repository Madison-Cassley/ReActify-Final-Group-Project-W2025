import pytest
from gpiozero import PWMLED, OutputDevice
from gpiozero.pins.mock import MockFactory, MockPWMPin
#from grove.grove_voc_ec02_gas_sensor import GroveVOCeCO2GasSensor
#from grove.grove_sgp30 import GroveSGP30
from src.fire_air_quality_system.devices.CO2Sensor import GroveVOCeCO2Sensor, CO2Sensor

from src.common.devices.actuator import Action, Actuator
from src.common.devices.device_controller import DeviceController
from src.fire_air_quality_system.devices.fan import FanActuator
from src.fire_air_quality_system.devices.mocks import MockGroveVOCeCO2Sensor, MockRBGLedStickActuator
from src.common.devices.sensor import Measurement, Sensor
from src.fire_air_quality_system.devices.RGBLedStick import RBGLedStickActuator

from src.fire_air_quality_system.devices.examples import LEDBrightnessActuator, LEDPulseActuator, LEDToggleActuator


@pytest.fixture
def mock_fan() -> OutputDevice:
    """Fixture mocking a Fan connected to GPIO 16 on the grove base hat."""
    return OutputDevice(pin=16, pin_factory=MockFactory())



@pytest.fixture
def mock_co2() -> GroveVOCeCO2Sensor:
    """Fixture mocking a GroveVOCeCO2Sensor device connected to i2c bus 4 of the reTerminal."""
    return MockGroveVOCeCO2Sensor(address=0x38, bus=4)

@pytest.fixture
def fan_actuator(mock_fan: OutputDevice) -> FanActuator:
    """Fixture actuator for the FAN_TOGGLE action."""
    fan = mock_fan
    action = Action.FAN_TOGGLE
    return FanActuator(device=fan, action=action, state=0)

@pytest.fixture
def led_toggle_actuator() -> RBGLedStickActuator:
    action = Action.RGB_LED_TOGGLE
    return MockRBGLedStickActuator(action)

@pytest.fixture
def led_red_actuator() -> MockRBGLedStickActuator:
    """Fixture actuator for the LED_RED action."""
    action = Action.RGB_LED_RED
    return MockRBGLedStickActuator(action)



# TODO: double check this is using your definition of temperature sensor
@pytest.fixture
def co2_sensor(mock_co2: GroveVOCeCO2Sensor) -> CO2Sensor:
    """Fixture sensor for the TEMPERATURE measurement."""
    device = mock_co2
    measurement = Measurement.CO2LEVEL
    return CO2Sensor(device=device, measurement=measurement)



# # TODO: double check this is using your definition of led brightness actuator
# @pytest.fixture
# def led_brightness_actuator(mock_rgb_led: PWMLED) -> RBGLedStickActuator:
#     """Fixture actuator for the LED_BRIGHTNESS action."""
#     led = mock_rgb_led
#     action = Action.RGB_LED_RED
#     return RBGLedStickActuator(device=led, action=action, state=0)



@pytest.fixture
def all_actuators(
    fan_actuator: FanActuator,
    led_toggle_actuator: MockRBGLedStickActuator,
    led_red_actuator: MockRBGLedStickActuator
) -> list[Actuator]:
    """A list of all available actuator fixtures."""
    return [fan_actuator, led_toggle_actuator, led_red_actuator]


@pytest.fixture
def all_sensors(
    co2_sensor: GroveVOCeCO2Sensor
) -> list[Sensor]:
    """A list of all available sensor fixtures."""
    return [co2_sensor]


@pytest.fixture
def device_controller(all_actuators: list[Actuator], all_sensors: list[Sensor]) -> DeviceController:
    """Fixture DeviceController instantiated with all available actuators and sensors."""
    return DeviceController(actuators=all_actuators, sensors=all_sensors)
