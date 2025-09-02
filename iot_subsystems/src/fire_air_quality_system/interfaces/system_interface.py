from interfaces import Interface
from interfaces import Interface
import asyncio
try:        
    import seeed_python_rpi.core as rt
    import seeed_python_rpi.acceleration as rt_accel
    import seeed_python_rpi.button as rt_btn
except:
    print("seeed_python_rpi imports not available if running on WSL")

class KeyboardInterface(Interface):
    """Implementation of the Interface class for a keyboard interface."""

    def __init__(self) -> None:
        """Initialize the interface class."""
        from sshkeyboard import listen_keyboard_manual, stop_listening

        self.listen_keyboard = listen_keyboard_manual
        self.stop_listening = stop_listening
        super().__init__()

    async def event_loop(self) -> None:
        """Runs an event loop that listens for keyboard button presses."""
        print("Waiting for keyboard input! Press F1, F2, F3, or O")
        await self.listen_keyboard(on_press=self.key_press, on_release=self.key_release)

    def end_event_loop(self) -> None:
        """See base class."""
        self.stop_listening()

    def key_press(self, key: str) -> None:
        """See base class."""
        return super().key_press(key)

    def key_release(self, key: str) -> None:
        """See base class."""
        return super().key_release(key)
    

class ReterminalInterface(Interface):
    """Implementation of the SystemInterface class for the Reterminal chassis."""

    def __init__(self) -> None:
        """Initialize the interface class."""
        super().__init__()
    # The "button" code here will be useful: 
    # https://github.com/Seeed-Studio/Seeed_Python_RPi?tab=readme-ov-file#accelerometer-and-buttons-test
    async def event_loop(self) -> None:
        """Runs an event loop that listens for reterminal button presses."""
        print("Waiting for keyboard input! Press F1, F2, F3, or O")
        device = rt.get_button_device()
        
        async for event in device.async_read_loop():
            buttonEvent = rt_btn.ButtonEvent(event)
            if buttonEvent.name != None:
                print(f"name={str(buttonEvent.name)} value={buttonEvent.value}")
                
                if (buttonEvent.value == 1):
                    self.key_press(buttonEvent.name.name)
                elif(buttonEvent.value == 0):
                    self.key_release(buttonEvent.name.name)
        
        pass

    def end_event_loop(self) -> None:
        """Terminates the event loop started by the event_loop method."""
        raise StopAsyncIteration

    def key_press(self, key: str) -> None:
        """See base class."""
        return super().key_press(key)

    def key_release(self, key: str) -> None:
        """See base class."""
        return super().key_release(key)