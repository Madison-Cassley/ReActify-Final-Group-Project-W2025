import random

from common.devices.sensor import Measurement, Reading, Sensor


class MockSoundSensor(Sensor):
    def __init__(self):
        self.measurement = Measurement.SOUND

    def read_sensor(self) -> Reading:
        value = random.randint(100, 300)
        return Reading(value=value, measurement=self.measurement)
