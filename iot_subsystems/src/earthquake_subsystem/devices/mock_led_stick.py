from common.devices.actuator import Action, Actuator, Command


class MockLEDStickActuator(Actuator):
    def __init__(self):
        self.action = Action.LED_TOGGLE
        self.state = 0.0

    def control_actuator(self, command: Command) -> bool:
        if command.action != self.action:
            return False
        self.state = command.data
        return True

    def turn_off(self):
        self.state = 0.0
