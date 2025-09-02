import logging
import os
import random

from common.devices.sensor import Sensor, Measurement, Reading

ENV = os.getenv("ENVIRONMENT", "DEVELOPMENT").upper()

if ENV == "PRODUCTION":
    import grove.i2c
    grove.i2c.Bus(1)
    from grove.grove_water_sensor import GroveWaterSensor  # real driver
else:
    class GroveWaterSensor:
        """
        Development stub for GroveWaterSensor.
        """
        def __init__(self, pin):
            self.pin = pin

        def read(self):
            """Simulate a raw water level sensor reading between calibration limits."""
            return random.uniform(RAW_DRY, RAW_WET)

        @property
        def value(self):
            #real driver uses .value; stub uses .read()
            return None

logger = logging.getLogger(__name__)

RAW_DRY = 0.0      #Raw reading when sensor is in air
RAW_WET = 675.0    #Raw reading when fully submerged (~5 cm)
SENSOR_LENGTH_CM = 5.0  #Physical sensor length in cm


def raw_to_cm(raw: float) -> float:
    """
    Convert raw sensor reading to water level in centimeters.
    Clamps raw to [RAW_DRY, RAW_WET] and linearly maps to [0, SENSOR_LENGTH_CM].
    """
    raw_clamped = max(RAW_DRY, min(raw, RAW_WET))
    return (raw_clamped - RAW_DRY) / (RAW_WET - RAW_DRY) * SENSOR_LENGTH_CM


class WaterLevelSensor(Sensor):
    def __init__(self, pin: int = 2) -> None:
        self.device = GroveWaterSensor(pin)
        self.measurement = Measurement.WATER_LEVEL

    def read_sensor(self) -> Reading:
        raw = getattr(self.device, "value", None)
        if raw is None:
            raw = self.device.read()
        level_cm = raw_to_cm(raw)
        logger.info(f"Water level: {level_cm:.2f}{self.measurement.unit}")
        return Reading(f"{level_cm:.2f}", self.measurement)
