import asyncio
from common.devices.actuator import Command, Action
from common.interfaces.reterminal import ReterminalInterface

class WaterFloodsReterminalInterface(ReterminalInterface):
    """Listen for the built-in ReTerminal F1/F2/F3 keys and invoke commands."""

    def __init__(self) -> None:
        super().__init__()
        self.dc = None  #set by WaterFloodsSystem
        self.azure = None

    def register_device_controller(self, dc) -> None:
        self.dc = dc

    def key_press(self, key: str) -> None:
        #F1 → buzzer ON for 3 s
        if key == "F1":
            self.dc.control_actuator(Command(Action.BUZZER_TOGGLE, 1))
            asyncio.create_task(self._turn_buzzer_off())

        #F2 → sweep servo to 180°
        elif key == "F2":
            self.dc.control_actuator(Command(Action.SERVO_ANGLE, 180))

        #F3 → take one reading from each sensor
        elif key == "F3":
            readings = self.dc.read_sensors()
            for r in readings:
                print(f"{r.measurement.name}: {r.value}{r.measurement.unit}")
            asyncio.create_task(self.azure.send_readings(readings))

    def key_release(self, key: str) -> None:
        #not used
        pass

    async def _turn_buzzer_off(self) -> None:
        await asyncio.sleep(3)
        self.dc.control_actuator(Command(Action.BUZZER_TOGGLE, 0))

    async def run(self) -> None:
        await self.event_loop()
