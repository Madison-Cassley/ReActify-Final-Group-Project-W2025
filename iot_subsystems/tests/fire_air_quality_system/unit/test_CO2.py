# TODO: replace these imports with your own imports, and delete `src/hvac_system/devices/examples.py` afterwards
#from hvac_system.devices.examples import HumiditySensor, TemperatureSensor
#from src.Alex_system.devices.CO2Sensor import CO2Sensor
from src.fire_air_quality_system.devices.mocks import MockGroveVOCeCO2Sensor


def test_co2_sensor_read_sensor_returns_reading(co2_sensor: MockGroveVOCeCO2Sensor):
    reading = co2_sensor.read_sensor()
    assert isinstance(reading.value, float)
    assert reading.measurement == co2_sensor.measurement
