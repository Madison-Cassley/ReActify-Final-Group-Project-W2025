# Water & Soil Monitoring Subsystem

**IoT Device Name:** `WaterFloodsSubSystem` :contentReference[oaicite:2]{index=2}:contentReference[oaicite:3]{index=3}

## Devices

This subsystem currently implements the following:

- **Soil Moisture Sensor** (GroveMoistureSensor)  
- **Water Level Sensor** (GroveWaterSensor)  
- **Buzzer** (ReTerminalBuzzerDevice)  
- **Servo Motor** (AngularServo)  

## Hardware --> GPIO Mapping

| Device                  | Hardware Module              | Base HAT Port       | Connection Type | Details            |
|-------------------------|------------------------------|---------------------|-----------------|--------------------|
| Soil Moisture Sensor    | Grove Soil Moisture Sensor   | A0                  | Analog          | Pin 0              |
| Water Level Sensor      | Grove Water Sensor           | A2                  | Analog          | Pin 2              |
| Buzzer                  | On-board ReTerminal Buzzer   | reTerminal Buzzer   | Digital         | Accessed via special permissions|
| Servo Motor             | Standard Servo on D5 port    | D5 (GPIO 12)        | PWM Digital     | Relay is on Pin 5, Servo signal is on Pin 12|


## Actions
- Buzzer beeps every second if moisture reaches above 80% (unhealthy)
- Servo will move 90 degrees to open a drain when water reaches 3.5cm or above and will close again once its below 3.5cm
- If both cases are met, both actuators will perform their action
