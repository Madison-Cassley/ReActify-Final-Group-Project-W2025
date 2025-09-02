# This software is intended for educational use by students and teachers in the
# the Computer Science department at John Abbott College.
# See the license disclaimer below and the project LICENSE file for more information.
# -----
# Copyright (C) 2025 michaelhaaf
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

# Note: To run tests, include "src.Alex_system" in "from"


from src.common.devices.sensor import Reading, Measurement
from src.common.iot import IOTDeviceClient
from azure.iot.device.aio import IoTHubDeviceClient 
from azure.iot.device import MethodResponse
#from Alex_system.devices.mocks import MockGroveVOCeCO2Sensor
from src.fire_air_quality_system.devices.CO2Sensor import CO2Sensor
from src.common.devices.actuator import Actuator, Action,Command
from src.common.devices.device_controller import DeviceController

import time
import json
from azure.iot.device import Message
import asyncio
import os
#Permits access to specific .env file and its content
from dotenv import load_dotenv
load_dotenv() # load env file into enviroment variables

class AzureDeviceClient(IOTDeviceClient):
    """IOT integrations with Azure Iot Hub."""
    deviceClient: IOTDeviceClient
    devices: DeviceController

    def __init__(self, device_controllers):
        self.devices = device_controllers
        connection_string = os.getenv("DEVICECONNECTIONSTRING")   
        print(connection_string)               
        self.deviceClient = IoTHubDeviceClient.create_from_connection_string(connection_string)  
        self.deviceClient.on_method_request_received = self.handle_method_request    

    async def connect(self) -> None:
        """Connects to IoTHub."""
        try:
            await self.deviceClient.connect()
            print("Connection successful")
        except:
            print("Unable to connect")
       
    async def send_reading(self, reading: Reading) -> None:
        """Sends reading to IoTHub."""          
        readingDictionary = {str(reading.measurement):str(reading.value)}        
        payload = json.dumps(readingDictionary)
        message = Message(payload)
        await self.deviceClient.send_message(message)  
        #print(message)      

    async def send_readings(self, readings: list[Reading]) -> None:
        """Sends readings to IoTHub."""
        
        for reading in readings:
            readingDictionary = {str(reading.measurement):str(reading.value)}        
            payload = json.dumps(readingDictionary)
            message = Message(payload)                     
            await self.deviceClient.send_message(message)
            #print(message)        

    # Define the method handler
    async def handle_method_request(self, method_request):       
        if method_request.name == "ToggleFan":           
            payload = method_request.payload
            fanState = payload.get("FanState", None)           
            status = 200
            self.ProcessAndExecuteActuator("FAN",fanState)
        
        elif method_request.name == "ToggleLED":
            payload = method_request.payload
            rgbState = payload.get("LEDState", None)           
            status = 200
            self.ProcessAndExecuteActuator("RGB",rgbState)
        else:
            payload ={"results": False}
            status = 404

        method_response = MethodResponse.create_from_method_request(
            method_request, status, payload
        )
        await self.deviceClient.send_method_response(method_response)
    
    def ProcessAndExecuteActuator(self,deviceName,state):        
                
        if (deviceName == "FAN"):
            try:
                if(state == "ON"):                
                    command = Command(Action.FAN_TOGGLE, 1)                  
                    self.devices.control_actuator(command)                   
                elif (state == "OFF"):
                    command = Command(Action.FAN_TOGGLE, 0)                   
                    self.devices.control_actuator(command)                   
            except Exception as msg:
                print("Unable to toggle fan. Details:", msg)        
        elif (deviceName == "RGB"):
            try:
                if(state == "ON"):
                    command = Command(Action.RGB_LED_RED, 0)                   
                    self.devices.control_actuator(command)
                    command = Command(Action.RGB_LED_YELLOW, 0)                   
                    self.devices.control_actuator(command)
                    command = Command(Action.RGB_LED_GREEN, 0)                   
                    self.devices.control_actuator(command)

                    command = Command(Action.RGB_LED_TOGGLE, 1)                  
                    self.devices.control_actuator(command) 

                
                elif (state == "RED"):
                    command = Command(Action.RGB_LED_TOGGLE, 0)                  
                    self.devices.control_actuator(command) 
                    command = Command(Action.RGB_LED_YELLOW, 0)                   
                    self.devices.control_actuator(command)
                    command = Command(Action.RGB_LED_GREEN, 0)                   
                    self.devices.control_actuator(command)

                    command = Command(Action.RGB_LED_RED, 1)                   
                    self.devices.control_actuator(command)
                
                elif (state == "YELLOW"):
                    print("Turning light yellow")
                    command = Command(Action.RGB_LED_TOGGLE, 0)                  
                    self.devices.control_actuator(command) 
                    command = Command(Action.RGB_LED_YELLOW, 0)                   
                    self.devices.control_actuator(command)
                    command = Command(Action.RGB_LED_GREEN, 0)                   
                    self.devices.control_actuator(command)

                    command = Command(Action.RGB_LED_YELLOW, 1)                   
                    self.devices.control_actuator(command)
                
                elif (state == "GREEN"):
                    print("Turning light green")                    
                    command = Command(Action.RGB_LED_TOGGLE, 0)                  
                    self.devices.control_actuator(command) 
                    command = Command(Action.RGB_LED_RED, 0)                   
                    self.devices.control_actuator(command)
                    command = Command(Action.RGB_LED_YELLOW, 0)                   
                    self.devices.control_actuator(command)

                    command = Command(Action.RGB_LED_GREEN, 1)                   
                    self.devices.control_actuator(command)
                
                elif (state == "OFF"):
                    command = Command(Action.RGB_LED_TOGGLE, 0)                   
                    self.devices.control_actuator(command)
                    command = Command(Action.RGB_LED_RED, 0)                   
                    self.devices.control_actuator(command)
                    command = Command(Action.RGB_LED_YELLOW, 0)                   
                    self.devices.control_actuator(command)
                    command = Command(Action.RGB_LED_GREEN, 0)                   
                    self.devices.control_actuator(command)
            
            except Exception as msg:
                print("Unable to toggle rgb led. Details:", msg) 


async def main(): 
    client = AzureDeviceClient()
    await client.connect()
    print("Device online and waiting for C2D method calls...")    
    
    while True:
        await asyncio.sleep(1)
       

if __name__ == "__main__":
    """
    Usage:
        $ PYTHONPATH=${PYTHONPATH}:src python src/Alex_system/iot/azure_device_client.py
    Alternatively:
        $ export PYTHONPATH=${PYTHONPATH}:${HOME}/path-to-repository/src
        $ python src/hvac_system/devices/fan.py
    """
    try:        
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Shutting down...")
        pass