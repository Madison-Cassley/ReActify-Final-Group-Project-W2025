import logging

from gpiozero import MotionSensor

from common.devices.sensor import Measurement, Reading, Sensor

logger = logging.getLogger(__name__)


class PIRSensor(Sensor):
    """Implementation for Grove PIR Motion Sensor."""

    device: MotionSensor
    measurement: Measurement

    def __init__(self, pin: int = 22) -> None:
        """Initialize the motion sensor on the specified GPIO pin."""
        self.device = MotionSensor(pin)
        self.measurement = Measurement.MOTION

    def read_sensor(self) -> Reading:
        """Read sensor to detect motion (1.0 if motion, 0.0 otherwise)."""
        detected = self.device.motion_detected
        # print(f"[DEBUG] motion_detected={detected}")
        value = 1.0 if detected else 0.0
        reading = Reading(value=value, measurement=self.measurement)
        return reading
