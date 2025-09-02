import logging
import os
import random

ENV = os.getenv("ENVIRONMENT", "DEVELOPMENT").upper()

if ENV == "PRODUCTION":
    import grove.i2c
    grove.i2c.Bus(1)

    from grove.grove_moisture_sensor import GroveMoistureSensor  # real driver
else:
    class GroveMoistureSensor:
        def __init__(self, pin):
            self.pin = pin

        def read(self):
            return random.uniform(0, 100)

from common.devices.sensor import Sensor, Reading, Measurement

logger = logging.getLogger(__name__)

class SoilMoistureSensor(Sensor):
    def __init__(self, pin: int = 0) -> None:
        #grove library uses 0 for A0
        self.device = GroveMoistureSensor(pin)
        self.measurement = Measurement.SOIL_MOISTURE

    DRY_ADC = 3000.0   #0% moisture
    WET_ADC = 1500.0   #100% moisture

    def read_sensor(self) -> Reading:
        raw = getattr(self.device, "moisture", None)
        if raw is None:
            raw = self.device.read()
        raw_clamped = max(min(raw, self.DRY_ADC), self.WET_ADC)

        percent = (self.DRY_ADC - raw_clamped) / (self.DRY_ADC - self.WET_ADC) * 100
        percent = round(max(0.0, min(percent, 100.0)), 1)

        logger.info(f"Soil moisture: {percent}{self.measurement.unit}")
        return Reading(f"{percent:.1f}", self.measurement)