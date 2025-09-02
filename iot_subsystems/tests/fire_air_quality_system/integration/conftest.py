from src.common.devices.sensor import Reading
from src.fire_air_quality_system.interfaces import Interface
from src.fire_air_quality_system.iot.azure_device_client import AzureDeviceClient


class MockInterface(Interface):
    async def mock_event(self) -> dict:
        return {}

    async def event_loop(self) -> None:
        event = await self.mock_event()
        if event.get("value") == 1:
            self.key_press(event["key"])
        elif event.get("value") == 0:
            self.key_release(event["key"])

    def end_event_loop(self) -> None:
        pass

    def key_press(self, key: str) -> None:
        return super().key_press(key)

    def key_release(self, key: str) -> None:
        return super().key_release(key)


class MockIOTDeviceClient(AzureDeviceClient):
    async def connect(self) -> None:
        pass

    async def send_reading(self, reading: Reading) -> None:
        pass