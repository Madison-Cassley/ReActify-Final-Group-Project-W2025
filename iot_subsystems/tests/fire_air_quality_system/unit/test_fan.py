from src.common.devices.actuator import Action, Command
from src.fire_air_quality_system.devices.fan import FanActuator


def test_control_actuator_return_true_off_to_on(fan_actuator: FanActuator):
    fan_on = Command(Action.FAN_TOGGLE, 1)
    assert fan_actuator.control_actuator(fan_on)


def test_control_actuator_return_true_on_to_off(fan_actuator: FanActuator):
    fan_on = Command(Action.FAN_TOGGLE, 1)
    fan_off = Command(Action.FAN_TOGGLE, 0)
    fan_actuator.control_actuator(fan_on)
    assert fan_actuator.control_actuator(fan_off)


def test_control_actuator_return_false_on_to_on(fan_actuator: FanActuator):
    fan_on = Command(Action.FAN_TOGGLE, 1)
    fan_actuator.control_actuator(fan_on)
    assert not fan_actuator.control_actuator(fan_on)
    # # TODO: remote this last assert when fan_actuator implemented
    # assert False


def test_control_actuator_return_false_off_to_off(fan_actuator: FanActuator):
    """TESTING THE DOCSTRING"""
    fan_off = Command(Action.FAN_TOGGLE, 0)
    fan_actuator.control_actuator(fan_off)
    assert not fan_actuator.control_actuator(fan_off)
    # # TODO: remote this last assert when fan_actuator implemented
    # assert False
