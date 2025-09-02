# Project Brainstorming

Once you are finished brainstorming your project ideas, fill in each of the sections below. You can continually update this project up to the morning of March 10th (the deadline).

**NOTE:** you should delete the initial sentences provided for each section (only include your own writing).

## Purpose

The **Smart Disaster Alert & Response System** is designed to detect and respond to environmental hazards such as fires, floods, and earthquakes. The system will use various sensors and actuators to monitor conditions, trigger safety responses, and notify users through a mobile app. This solution aims to increase safety and response efficiency by automating hazard detection and taking real-time actions before a disaster escalates.

## Subsystems

### Subsystem 1: Fire & Air Quality Monitoring

This subsystem is responsible for detecting fire risks, monitoring air quality, and triggering cooling/alerts in case of high temperature or smoke. It ensures that hazardous conditions are recognized early and proper actions are taken.

#### Devices

| **Component** | **Interface Type** | **Documentation** |  
|--------------|------------------|------------------|  
| **AHT20 Temp & Humidity Sensor** | I2C | [Grove AHT20 Temp & Humidity Sensor](https://wiki.seeedstudio.com/Grove-AHT20-I2C-Industrial-Grade-Temperature&Humidity-Sensor/) |  
| **Sound Sensor (Noise Detector for Smoke Alarms)** | Analog | [Grove Loudness Sensor](https://wiki.seeedstudio.com/Grove-Loudness_Sensor/) |  
| **Cooling Fan** | Digital (Relay) | [5V Relay Control for Cooling Fan](https://www.circuitbasics.com/5v-relays-in-the-raspberry-pi/) |  
| **RGB LED Stick** | PWM | [RGB LED Strip](https://wiki.seeedstudio.com/Grove-RGB_LED_Stick-10-WS2813_Mini/) |  

### Subsystem 2: Flood & Water Level Detection

This subsystem detects flooding risks by monitoring water levels and soil moisture. It automatically closes drainage systems and sends flood alerts if dangerous conditions are detected.

#### Devices

| **Component** | **Interface Type** | **Documentation** |  
|--------------|------------------|------------------|  
| **Water Level Sensor** | Analog | [Grove Water Level Sensor](https://wiki.seeedstudio.com/Grove-Water-Level-Sensor/) |  
| **Soil Moisture Sensor** | Analog | [Grove Capacitive Moisture Sensor](https://wiki.seeedstudio.com/Grove-Capacitive_Moisture_Sensor-Corrosion-Resistant/) |  
| **MG90S 180° Micro Servo** (Drainage Control) | PWM | [MG90S Servo Motor](https://makersportal.com/blog/2020/3/21/raspberry-pi-servo-panning-camera) |  
| **reTerminal’s Built-in Buzzer** | I2C (I/O Expander) | [reTerminal Buzzer](https://wiki.seeedstudio.com/reTerminal-hardware-interfaces-usage/#buzzer) |  

### Subsystem 3: Earthquake Detection & Structural Response

This subsystem monitors vibrations and movement to detect earthquakes. If abnormal movement is detected, it automatically locks doors and flashes warning lights.

#### Devices

| **Component** | **Interface Type** | **Documentation** |  
|--------------|------------------|------------------|  
| **reTerminal's Built-in Accelerometer** | 12C | [reTerminal Accelerometer](https://wiki.seeedstudio.com/reTerminal-hardware-interfaces-usage/#accelerometer) |  
| **PIR Motion Sensor** | Digital | [Grove PIR Motion Sensor](https://wiki.seeedstudio.com/Grove-Adjustable_PIR_Motion_Sensor/) |  
| **Magnetic Door Sensor (Reed Switch)** | Digital | [Magnetic Reed Switch](https://wiki.seeedstudio.com/Grove-Magnetic_Switch/) |  
| **RGB LED Stick** | PWM | [RGB LED Strip](https://wiki.seeedstudio.com/Grove-RGB_LED_Stick-10-WS2813_Mini/) | 
