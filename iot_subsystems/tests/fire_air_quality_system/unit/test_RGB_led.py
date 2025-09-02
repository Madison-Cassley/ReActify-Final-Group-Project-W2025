from src.common.devices.actuator import Action, Command

# TODO: replace these imports with your own imports, and delete `src/hvac_system/devices/examples.py` afterwards
#from hvac_system.devices.examples import LEDBrightnessActuator, LEDToggleActuator
from src.fire_air_quality_system.devices.RGBLedStick import RBGLedStickActuator


def test_control_actuator_return_true_off_to_on(led_toggle_actuator: RBGLedStickActuator):
    rgb_led_on = Command(Action.RGB_LED_TOGGLE, 1)       
    assert led_toggle_actuator.control_actuator(rgb_led_on)


def test_control_actuator_return_true_on_to_off(led_toggle_actuator: RBGLedStickActuator):
    rgb_led_on = Command(Action.RGB_LED_TOGGLE, 1)
    rgb_led_off = Command(Action.RGB_LED_TOGGLE, 0)
    led_toggle_actuator.control_actuator(rgb_led_on)
    assert led_toggle_actuator.control_actuator(rgb_led_off)


def test_control_actuator_return_false_on_to_on(led_toggle_actuator: RBGLedStickActuator):
    rgb_led_on = Command(Action.RGB_LED_TOGGLE, 1)
    led_toggle_actuator.control_actuator(rgb_led_on)
    assert not led_toggle_actuator.control_actuator(rgb_led_on)
    # # TODO: remove this last assert when led_toggle_actuator implemented
    # assert False


def test_control_actuator_return_false_off_to_off(led_toggle_actuator: RBGLedStickActuator):
    rgb_led_off = Command(Action.RGB_LED_TOGGLE, 0)
    led_toggle_actuator.control_actuator(rgb_led_off)
    assert not led_toggle_actuator.control_actuator(rgb_led_off)


def test_control_actuator_return_true_led_red_off_to_on(led_toggle_actuator: RBGLedStickActuator):
    rgb_led_on = Command(Action.RGB_LED_RED, 1)   
    assert led_toggle_actuator.control_actuator(rgb_led_on)


def test_control_actuator_return_true_led_red_on_off(led_toggle_actuator: RBGLedStickActuator):
    rgb_led_on = Command(Action.RGB_LED_TOGGLE, 1)
    rgb_led_off = Command(Action.RGB_LED_RED, 0)
    led_toggle_actuator.control_actuator(rgb_led_on)
    assert led_toggle_actuator.control_actuator(rgb_led_off)


def test_control_actuator_return_false_led_red_on_to_on(led_toggle_actuator: RBGLedStickActuator):
    rgb_led_on = Command(Action.RGB_LED_RED, 1)   
    led_toggle_actuator.control_actuator(rgb_led_on)
    assert not led_toggle_actuator.control_actuator(rgb_led_on)


def test_control_actuator_return_false_led_red_off_to_off(led_toggle_actuator: RBGLedStickActuator):  
    rgb_led_off = Command(Action.RGB_LED_RED, 0)
    led_toggle_actuator.control_actuator(rgb_led_off)
    assert not led_toggle_actuator.control_actuator(rgb_led_off)
