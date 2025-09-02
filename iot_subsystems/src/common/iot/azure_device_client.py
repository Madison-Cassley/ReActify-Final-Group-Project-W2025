import os
import json
import asyncio
import logging

from dotenv import load_dotenv
from azure.iot.device.aio import IoTHubDeviceClient
from azure.iot.device import Message

from common.devices.sensor import Reading
from common.iot import IOTDeviceClient
from azure.iot.device import MethodResponse
from common.devices.actuator import Actuator, Action,Command
from common.devices.device_controller import DeviceController


logger = logging.getLogger(__name__)


class AzureDeviceClient(IOTDeviceClient):
    """Unified Azure IoT Hub client with Device Twin + D2C support."""

    devices: DeviceController

    def __init__(self, device_controllers = []):
        load_dotenv()
        conn_str = (
            os.getenv("IOT_DEVICE_CONNECTION_STRING") or
            os.getenv("DEVICECONNECTIONSTRING") or
            os.getenv("IOTHUB_CONNECTION_STRING")
        )

        if not conn_str:
            raise ValueError("No valid IoT connection string found in .env")

        self.devices = device_controllers
        self.client = IoTHubDeviceClient.create_from_connection_string(conn_str)
        self.telemetry_interval = 5  
        self.client.on_method_request_received = self.handle_method_request  

    async def connect(self) -> None:
        logger.info("[AZURE] Connecting to Azure IoT Hub...")
        await self.client.connect()
        logger.info("[AZURE] Connected.")

        self.client.on_twin_desired_properties_patch_received = self._handle_twin_patch

        twin = await self.client.get_twin()
        desired = twin.get("desired", {})
        self._parse_twin(desired)

    def _parse_twin(self, patch: dict) -> None:
        new_val = patch.get("telemetryInterval")
        if isinstance(new_val, int) and new_val > 0:
            self.telemetry_interval = new_val
            logger.info(f"[AZURE] Telemetry interval updated to {self.telemetry_interval} seconds.")
        else:
            logger.info("[AZURE] No valid telemetryInterval in patch.")

    def _handle_twin_patch(self, patch: dict) -> None:
        logger.info(f"[AZURE] Twin patch received: {patch}")
        self._parse_twin(patch)

    def get_interval(self) -> int:
        return self.telemetry_interval

    async def send_reading(self, reading: Reading) -> None:
        msg = Message(json.dumps({
            "value": reading.value,
            "measurement": reading.measurement.name
        }))
        msg.custom_properties["measurement"] = reading.measurement.name
        logger.info(f"[AZURE] Sending: {msg}")
        await self.client.send_message(msg)

    async def send_readings(self, readings: list[Reading]) -> None:
        for r in readings:
            await self.send_reading(r)
            await asyncio.sleep(1.5) 

    # Define the method handler
    async def handle_method_request(self, method_request):
        print("handle_method_request called")
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
        elif method_request.name == "ToggleLEDStick":
            payload = method_request.payload
            stickState = payload.get("LEDState", None)           
            status = 200
            self.ProcessAndExecuteActuator("LEDSTICK",stickState)
        else:
            payload ={"results": False}
            status = 404

        method_response = MethodResponse.create_from_method_request(
            method_request, status, payload
        )
        await self.client.send_method_response(method_response)

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
        elif (deviceName == "LEDSTICK"):
            try:
                if(state == "ON"):
                    command = Command(Action.LED_TOGGLE, 1.0)
                    self.devices.control_actuator(command)

                    asyncio.create_task(self.auto_turn_off_ledstick())

                elif(state == "OFF"):
                    command = Command(Action.LED_TOGGLE, 0.0)
                    self.devices.control_actuator(command)

            except Exception as msg:
                print("Unable to toggle LED stick. Details:", msg)

    async def auto_turn_off_ledstick(self):
        await asyncio.sleep(3)
        print("Auto turning off LED stick after 3 seconds")
        try:
            command = Command(Action.LED_TOGGLE, 0.0)
            self.devices.control_actuator(command)
        except Exception as e:
            print("Auto-off failed:", e)
