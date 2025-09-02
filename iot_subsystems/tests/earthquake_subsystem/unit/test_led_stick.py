# Tests mock rpi_ws2813.PixelStrip using pytest's monkeypatch fixture 
# https://docs.pytest.org/en/stable/how-to/monkeypatch.html
from common.devices.actuator import Command, Action
from earthquake_subsystem.devices.led_stick import LEDStickActuator


def test_led_stick_pulses_when_action_matches(monkeypatch):
    """Test that LEDStickActuator pulses when given the correct action."""
    # mock PixelStrip methods to avoid hardware
    monkeypatch.setattr("earthquake_subsystem.devices.led_stick.PixelStrip", lambda *a, **k: type(
        "MockStrip", (), {
            "begin": lambda self: None,
            "setPixelColor": lambda self, i, c: None,
            "show": lambda self: None
        }
    )())

    actuator = LEDStickActuator(pin=18)
    command = Command(action=Action.LED_PULSE, data=1.0)
    assert actuator.control_actuator(command) is True


def test_led_stick_returns_false_for_wrong_action(monkeypatch):
    """Test that LEDStickActuator ignores incorrect actions."""
    monkeypatch.setattr("earthquake_subsystem.devices.led_stick.PixelStrip", lambda *a, **k: type(
        "MockStrip", (), {
            "begin": lambda self: None,
            "setPixelColor": lambda self, i, c: None,
            "show": lambda self: None
        }
    )())

    actuator = LEDStickActuator(pin=18)
    command = Command(action=Action.FAN_TOGGLE, data=1.0)
    assert actuator.control_actuator(command) is False