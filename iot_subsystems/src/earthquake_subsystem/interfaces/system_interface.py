from common.interfaces import Interface

try:
    import seeed_python_rpi.button as rt_btn
    import seeed_python_rpi.core as rt
except ImportError:
    rt = None
    rt_btn = None


class KeyboardInterface(Interface):
    def __init__(self) -> None:
        from sshkeyboard import listen_keyboard_manual, stop_listening

        self.listen_keyboard = listen_keyboard_manual
        self.stop_listening = stop_listening
        super().__init__()

    async def event_loop(self) -> None:
        print("Keyboard Mode: Press F1/F2/F3")
        await self.listen_keyboard(on_press=self.key_press, on_release=self.key_release)

    def end_event_loop(self) -> None:
        self.stop_listening()

    def key_press(self, key: str) -> None:
        key = self.normalize_key(key)
        if "on_press" in self.callbacks:
            self.callbacks["on_press"](key)

    def key_release(self, key: str) -> None:
        key = self.normalize_key(key)
        if "on_release" in self.callbacks:
            self.callbacks["on_release"](key)

    def normalize_key(self, key: str) -> str:
        mapping = {"f1": "F1", "f2": "F2", "f3": "F3"}
        return mapping.get(key.lower(), key)


class ReterminalInterface(Interface):
    def __init__(self) -> None:
        if rt is None or rt_btn is None:
            raise RuntimeError(
                "Reterminal libraries not loaded. Please install seeed-python-rpi and run on reTerminal."
            )
        super().__init__()

    async def event_loop(self) -> None:
        print("Reterminal Mode: Press F1/F2/F3")
        device = rt.get_button_device()
        async for event in device.async_read_loop():
            buttonEvent = rt_btn.ButtonEvent(event)
            if buttonEvent.name is not None:
                if buttonEvent.value == 1:
                    self.key_press(buttonEvent.name.name)
                elif buttonEvent.value == 0:
                    self.key_release(buttonEvent.name.name)

    def end_event_loop(self) -> None:
        raise StopAsyncIteration

    def key_press(self, key: str) -> None:
        if "on_press" in self.callbacks:
            self.callbacks["on_press"](key)

    def key_release(self, key: str) -> None:
        if "on_release" in self.callbacks:
            self.callbacks["on_release"](key)
