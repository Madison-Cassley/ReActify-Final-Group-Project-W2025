# Earthquake Subsystem
This subsystem monitors earthquake-like activity using a combination of motion, sound, and visual indicators. It is one of the subsystems in our IoT Farm and is built to demonstrate real-time environmental reactivity.

---

## IoT Configuration

- **IoT Device Name:** `earthquake-subsystem`
- **Connected to IoT Hub:** `rania-iot-hub`

---

## Implemented Devices

| Device          | Description                          | GPIO / Channel | Type     | Extra Info           |
|-----------------|--------------------------------------|----------------|----------|-----------------------|
| PIR Sensor      | Detects motion via infrared          | D22            | Digital  | Uses `gpiozero`       |
| Sound Sensor    | Detects loud environmental noises    | A0 (Channel 0) | Analog   | Uses `grove.adc`      |
| LED Stick       | Visual output for warnings (purple)  | D18            | Digital  | 10 LEDs, `rpi_ws281x` |

---

- When **motion** is detected: PIR sensor reading logs `1.0`
- When **sound is detected**: SoundSensor logs the raw analog value (e.g. 200), useful for visualizing ambient noise levels
- When **LED pulse** action is sent, all LEDs flash **purple** for 3 seconds, then turn off

All devices follow OOP conventions, inheriting from `Sensor` or `Actuator` base classes.

---

## Tests

Each device has a full set of **unit tests** using `pytest` and `monkeypatch` for mocking hardware:

- `test_sound_sensor.py`
- `test_pir_sensor.py`
- `test_led_stick.py`

All tests pass:

```bash
PYTHONPATH=iot_subsystems/src pytest iot_subsystems/tests/earthquake_subsystem/unit/