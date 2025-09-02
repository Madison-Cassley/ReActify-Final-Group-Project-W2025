from earthquake_subsystem.devices.pir_sensor import PIRSensor


class MockPIR:
    def __init__(self, detected: bool):
        self._detected = detected

    @property
    def motion_detected(self):
        return self._detected


def test_pir_sensor_detects_motion(monkeypatch):
    """Test PIRSensor returns 1.0 when motion is detected."""
    monkeypatch.setattr("earthquake_subsystem.devices.pir_sensor.MotionSensor", lambda pin: MockPIR(True))
    sensor = PIRSensor(pin=22)
    reading = sensor.read_sensor()

    assert reading.value == 1.0
    assert reading.measurement == sensor.measurement


def test_pir_sensor_detects_no_motion(monkeypatch):
    """Test PIRSensor returns 0.0 when no motion is detected."""
    monkeypatch.setattr("earthquake_subsystem.devices.pir_sensor.MotionSensor", lambda pin: MockPIR(False))
    sensor = PIRSensor(pin=22)
    reading = sensor.read_sensor()

    assert reading.value == 0.0
    assert reading.measurement == sensor.measurement