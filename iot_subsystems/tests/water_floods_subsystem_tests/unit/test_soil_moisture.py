import os
import pytest

# force DEV mode so we hit the mock
os.environ["ENVIRONMENT"] = "DEVELOPMENT"

from src.water_floods_subsystem.devices.soil_moisture import SoilMoistureSensor

def test_read_sensor_returns_valid_reading():
    sensor = SoilMoistureSensor(pin=0)
    reading = sensor.read_sensor()
    #should have a numeric string value and the right measurement name
    assert isinstance(reading.value, str)
    assert float(reading.value) >= 0.0
    assert reading.measurement.name == "SOIL_MOISTURE"
