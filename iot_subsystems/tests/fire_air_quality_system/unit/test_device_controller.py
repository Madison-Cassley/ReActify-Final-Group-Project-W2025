from src.common.devices.actuator import Action, Actuator, Command
from src.common.devices.device_controller import DeviceController
from src.common.devices.sensor import Measurement
from src.fire_air_quality_system.devices.fan import FanActuator



def test_control_actuator_changes_correct_actuator_state(device_controller: DeviceController, fan_actuator: FanActuator, led_toggle_actuator: Actuator
):
    print(device_controller.actuators)
    fan_on = Command(Action.FAN_TOGGLE, 1)
    device_controller.control_actuator(fan_on)    
    assert fan_actuator.device.value == 1
    #assert led_toggle_actuator.device.value == 0

    led_on = Command(Action.RGB_LED_TOGGLE, 1)
    device_controller.control_actuator(led_on)
    assert fan_actuator.device.value == 1
    #assert led_toggle_actuator.device.value == 1

    fan_off = Command(Action.FAN_TOGGLE, 0)
    device_controller.control_actuator(fan_off)
    assert fan_actuator.device.value == 0
    #assert led_toggle_actuator.device.value == 1

    led_off = Command(Action.RGB_LED_TOGGLE, 0)
    device_controller.control_actuator(led_off)
    assert fan_actuator.device.value == 0
    #assert led_toggle_actuator.device.value == 0


def test_read_sensors_returns_readings_from_all_sensors(device_controller: DeviceController):
    readings = device_controller.read_sensors()
    assert len([r for r in readings if r.measurement == Measurement.CO2LEVEL]) == 1    


def test_read_sensor_returns_reading_only_matching_measurement(device_controller: DeviceController):
    co2_readings = device_controller.read_sensor(Measurement.CO2LEVEL)

    assert len(co2_readings) == 1
    assert len(co2_readings) == len([r for r in co2_readings if r.measurement == Measurement.CO2LEVEL])
