import asyncio
import logging
from azure.iot.device import MethodResponse                                # ← new
from common.devices.device_controller import DeviceController
from water_floods_subsystem.devices.soil_moisture import SoilMoistureSensor
from water_floods_subsystem.devices.water_level import WaterLevelSensor
from water_floods_subsystem.devices.servo_motor import ServoActuator
from water_floods_subsystem.devices.buzzer import BuzzerActuator
from water_floods_subsystem.interfaces.keyboard import WaterFloodsReterminalInterface
from common.iot.azure_device_client import AzureDeviceClient
from common.devices.actuator import Command, Action

logger = logging.getLogger(__name__)

class WaterFloodsSystem:
    def __init__(self):
        # build sensors & actuators
        sensors = [
            SoilMoistureSensor(pin=0),
            WaterLevelSensor(pin=3),
        ]
        actuators = [
            ServoActuator(pin=12),
            BuzzerActuator(),
        ]
        self.device_controller = DeviceController(sensors, actuators)

        # use the shared/common Azure IoT client
        self.azure = AzureDeviceClient()

        # optional manual interface
        self.interface = WaterFloodsReterminalInterface()
        self.interface.register_device_controller(self.device_controller)
        self.interface.azure = self.azure

    async def _periodic_publish(self, interval: int = 5) -> None:
        while True:
            readings = self.device_controller.read_sensors()
            logger.info(
                "Publishing: %s",
                ", ".join(f"{r.measurement.name}={r.value}" for r in readings)
            )
            await self.azure.send_readings(readings)
            await asyncio.sleep(interval)

    async def _monitor_and_actuate(self) -> None:
        buzzer_state = 0
        last_servo_angle = None

        while True:
            readings = self.device_controller.read_sensors()
            buzzer_active = False

            for r in readings:
                if r.measurement.name == "WATER_LEVEL":
                    lvl = float(r.value)
                    target_angle = 0 if lvl >= 3.5 else 180
                    if target_angle != last_servo_angle:
                        logger.info(f"Actuating servo → {target_angle}° (water={lvl}cm)")
                        self.device_controller.control_actuator(
                            Command(Action.SERVO_ANGLE, target_angle)
                        )
                        last_servo_angle = target_angle

                elif r.measurement.name == "SOIL_MOISTURE":
                    if float(r.value) >= 80:
                        buzzer_active = True

            if buzzer_active:
                buzzer_state ^= 1
                logger.info(f"Actuating buzzer → {buzzer_state}")
                self.device_controller.control_actuator(
                    Command(Action.BUZZER_TOGGLE, buzzer_state)
                )
            else:
                if buzzer_state != 0:
                    logger.info("Turning buzzer off")
                    self.device_controller.control_actuator(
                        Command(Action.BUZZER_TOGGLE, 0)
                    )
                    buzzer_state = 0

            await asyncio.sleep(1)

    async def _on_c2d_method(self, method_request) -> None:  
        """
        Handle SetServoAngle & ToggleBuzzer direct-method calls from your MAUI app.
        """
        payload = method_request.payload or {}
        name    = method_request.name
        status  = 200
        resp    = {"status": "ok"}

        if name == "SetServoAngle":
            angle = int(payload.get("data", 0))
            self.device_controller.control_actuator(
                Command(Action.SERVO_ANGLE, angle)
            )
        elif name == "ToggleBuzzer":
            state = int(payload.get("data", 0))
            self.device_controller.control_actuator(
                Command(Action.BUZZER_TOGGLE, state)
            )
        else:
            status = 404
            resp   = {"status": "unknown method"}

        # send the method response back
        method_response = MethodResponse.create_from_method_request(
            method_request, status=status, payload=resp
        )
        await self.azure.client.send_method_response(method_response)

    async def run(self) -> None:
        # connect to IoT Hub
        await self.azure.connect()

        # ─── Hook up your app’s buttons to the device ──────────────────────────
        # whenever the cloud invokes a method, route it to _on_c2d_method()
        self.azure.client.on_method_request_received = self._on_c2d_method  # :contentReference[oaicite:0]{index=0}

        # launch your two background loops
        asyncio.create_task(self._periodic_publish(interval=5))
        asyncio.create_task(self._monitor_and_actuate())

        # keep the manual interface alive (if you still want it)
        await self.interface.run()
