import os
import pytest

os.environ["ENVIRONMENT"] = "DEVELOPMENT"

from src.water_floods_subsystem.devices.servo_motor import ServoActuator
from src.common.devices.actuator import Command, Action

def test_servo_actuator_changes_state_and_idempotent():
    servo = ServoActuator(pin=18)
    #initial state should be 0
    assert servo.state == 0 or servo.state is None

    cmd90 = Command(Action.SERVO_ANGLE, 90)
    #first time: should change
    assert servo.control_actuator(cmd90) is True
    assert servo.state == 90

    #calling again with same angle: no change
    assert servo.control_actuator(cmd90) is False
