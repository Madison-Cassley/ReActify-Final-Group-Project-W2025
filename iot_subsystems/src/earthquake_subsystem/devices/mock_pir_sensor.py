import random

from common.devices.sensor import Measurement, Reading, Sensor


class MockPIRSensor(Sensor):
    def __init__(self):
        self.measurement = Measurement.MOTION

    def read_sensor(self) -> Reading:
        value = random.choice([0.0, 1.0])
        return Reading(value=value, measurement=self.measurement)
