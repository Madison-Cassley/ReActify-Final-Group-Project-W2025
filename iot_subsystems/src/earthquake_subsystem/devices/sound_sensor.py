import logging

from grove.adc import ADC

from common.devices.sensor import Measurement, Reading, Sensor

logger = logging.getLogger(__name__)


class SoundSensor(Sensor):
    """Sound sensor using Grove analog A0 port."""

    adc: ADC
    channel: int
    measurement: Measurement

    def __init__(self, channel: int = 0) -> None:
        """Initialize the sound sensor."""
        self.adc = ADC()
        self.channel = channel
        self.measurement = Measurement.SOUND

    def read_sensor(self) -> Reading:
        """Read and return sound intensity from ADC."""
        analog_value = self.adc.read(self.channel)
        # print(f"[DEBUG] raw analog_value={analog_value}")
        reading = Reading(value=analog_value, measurement=self.measurement)
        return reading
