import logging
import os
import random
import typing

from common.devices.actuator import Actuator, Command, Action

ENV = os.getenv("ENVIRONMENT", "PRODUCTION").upper()
if ENV == "PRODUCTION":
    import seeed_python_reterminal.core as rt

    class ReTerminalBuzzerDevice:
        @property
        def value(self) -> bool:
            return bool(rt.buzzer)

        @value.setter
        def value(self, on: bool) -> None:
            # in PRODUCTION this writes to sysfs
            rt.buzzer = on

else:
    class ReTerminalBuzzerDevice:
        def __init__(self):
            self._state = False

        @property
        def value(self) -> bool:
            return self._state

        @value.setter
        def value(self, on: bool) -> None:
            self._state = bool(on)
            #simulate a hardware write with a log
            logging.getLogger(__name__).info(f"[MOCK BUZZER] set to {self._state}")

logger = logging.getLogger(__name__)

class BuzzerActuator(Actuator):
    def __init__(self) -> None:
        super().__init__()
        self.device = ReTerminalBuzzerDevice()
        self.action = Action.BUZZER_TOGGLE
        self.state = 1 if self.device.value else 0

    def control_actuator(self, command: Command) -> bool:
        if command.action is not self.action:
            logger.warning(f"BuzzerActuator got wrong action: {command.action}")
            return False

        new_state = 1 if command.data else 0
        if new_state == self.state:
            return False

        self.device.value = bool(new_state)
        self.state = new_state
        state_str = "ON" if self.state else "OFF"
        logger.info(f"BUZZER_TOGGLE → {state_str}")
        return True
