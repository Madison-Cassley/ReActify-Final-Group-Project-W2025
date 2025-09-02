import logging
import os
from common.devices.actuator import Actuator, Command, Action

logger = logging.getLogger(__name__)

#A no-op stand-in for AngularServo if the real one errors out
class DummyServo:
    def __init__(self, *args, **kwargs):
        self._angle = 0

    @property
    def angle(self):
        return self._angle

    @angle.setter
    def angle(self, val):
        self._angle = val
        logger.info(f"[DummyServo] set angle to {val}°")


class ServoActuator(Actuator):
    def __init__(self, pin: int = 12) -> None:
        self.action = Action.SERVO_ANGLE
        try:
            #try the real servo
            from gpiozero import AngularServo
            dev = AngularServo(pin, min_angle=0, max_angle=180, initial_angle=0)
            logger.info(f"[ServoActuator] AngularServo attached to pin {pin}")
        except Exception as e:
            #fallback to dummy
            logger.warning(f"[ServoActuator] failed to init real servo ({e}), using DummyServo")
            dev = DummyServo()

        self.device = dev
        # evice.angle may be None if real servo failed; ensure a number
        self.state = getattr(dev, "angle", 0) or 0

    def control_actuator(self, command: Command) -> bool:
        if command.action is not self.action:
            logger.warning(f"ServoActuator got wrong action: {command.action}")
            return False
        if not (self.action.min_value <= command.data <= self.action.max_value):
            logger.error(f"{self.action.name} data {command.data} out of bounds")
            return False
        if command.data == self.state:
            return False

        #apply to whichever device we ended up with
        self.device.angle = command.data
        self.state = command.data
        logger.info(f"SERVO_ANGLE → {self.state}°")
        return True
