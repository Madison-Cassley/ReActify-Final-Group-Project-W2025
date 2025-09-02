import os
import pytest

os.environ["ENVIRONMENT"] = "DEVELOPMENT"

from src.water_floods_subsystem.devices.water_level import WaterLevelSensor

def test_read_sensor_returns_valid_reading():
    sensor = WaterLevelSensor(pin=2)
    reading = sensor.read_sensor()
    assert isinstance(reading.value, str)
    assert float(reading.value) >= 0.0
    assert reading.measurement.name == "WATER_LEVEL"
