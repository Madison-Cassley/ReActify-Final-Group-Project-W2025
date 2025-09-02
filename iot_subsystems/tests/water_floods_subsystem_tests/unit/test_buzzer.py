import os
import pytest

os.environ["ENVIRONMENT"] = "DEVELOPMENT"

from src.water_floods_subsystem.devices.buzzer import BuzzerActuator
from src.common.devices.actuator import Command, Action

def test_buzzer_actuator_toggles_and_idempotent(caplog):
    buzzer = BuzzerActuator()
    initial = buzzer.state

    #turn on
    cmd_on = Command(Action.BUZZER_TOGGLE, 1)
    assert buzzer.control_actuator(cmd_on) is True
    assert buzzer.state == 1

    #turning on again: no change
    assert buzzer.control_actuator(cmd_on) is False

    #turn off
    cmd_off = Command(Action.BUZZER_TOGGLE, 0)
    assert buzzer.control_actuator(cmd_off) is True
    assert buzzer.state == 0
