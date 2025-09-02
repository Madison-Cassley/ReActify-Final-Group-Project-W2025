# https://learn.adafruit.com/neopixels-on-raspberry-pi/python-usage
import logging

from rpi_ws281x import Color, PixelStrip

from common.devices.actuator import Action, Actuator, Command

logger = logging.getLogger(__name__)


class LEDStickDevice:
    def __init__(self, pin: int = 18, count: int = 10):
        self.count = count
        self.strip = PixelStrip(count, pin)
        self.strip.begin()

    def set_purple(self):
        """Set all LEDs to purple."""
        purple = Color(128, 0, 128)
        for i in range(self.count):
            self.strip.setPixelColor(i, purple)
        self.strip.show()

    def turn_off(self):
        """Turn off all LEDs."""
        for i in range(self.count):
            self.strip.setPixelColor(i, Color(0, 0, 0))
        self.strip.show()


class LEDStickActuator(Actuator):
    """LED Stick actuator that toggles all LEDs purple."""

    device: LEDStickDevice
    action: Action

    def __init__(self, pin: int = 18):
        self.device = LEDStickDevice(pin=pin)
        self.action = Action.LED_TOGGLE

    def control_actuator(self, command: Command) -> bool:
        if command.action != self.action:
            return False

        if command.data == 1.0:
            self.device.set_purple()
            logger.info("LEDStick: turned ON (purple)")
        else:
            self.device.turn_off()
            logger.info("LEDStick: turned OFF")

        return True

    def turn_off(self):
        self.device.turn_off()
