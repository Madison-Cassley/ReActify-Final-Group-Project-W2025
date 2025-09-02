from earthquake_subsystem.devices.sound_sensor import SoundSensor


def test_sound_sensor_reads_value(monkeypatch):
    """Test SoundSensor returns the correct reading value."""
    monkeypatch.setattr("earthquake_subsystem.devices.sound_sensor.ADC", lambda: type(
        "MockADC", (), {"read": lambda self, ch: 200}
    )())

    sensor = SoundSensor(channel=0)
    reading = sensor.read_sensor()

    assert reading.value == 200
    assert reading.measurement == sensor.measurement


def test_sound_sensor_reads_zero(monkeypatch):
    """Test SoundSensor returns zero when no input."""
    monkeypatch.setattr("earthquake_subsystem.devices.sound_sensor.ADC", lambda: type(
        "MockADC", (), {"read": lambda self, ch: 0}
    )())

    sensor = SoundSensor(channel=0)
    reading = sensor.read_sensor()

    assert reading.value == 0
    assert reading.measurement == sensor.measurement