import pytest
from asyncmock import AsyncMock
from logot import Logot, logged
from common.iot.azure_device_client import AzureDeviceClient
from src.Alex_system.devices.device_controller import DeviceController
from src.Alex_system.interfaces import Interface
from src.Alex_system.system import System
from .conftest import MockInterface, MockIOTDeviceClient


# class MockInterface(Interface):
#     async def mock_event(self) -> dict:
#         return {}

#     async def event_loop(self) -> None:
#         event = await self.mock_event()
#         if event.get("value") == 1:
#             print("Mock key pressed")
#             self.key_press(event["key"])
#         elif event.get("value") == 0:
#             print("Mock key released")
#             self.key_release(event["key"])

#     def end_event_loop(self) -> None:
#         pass

#     def key_press(self, key: str) -> None:
#         return super().key_press(key)

#     def key_release(self, key: str) -> None:
#         return super().key_release(key)


@pytest.fixture
def mock_interface() -> Interface:
    return MockInterface()


@pytest.fixture
def iot_device_client() -> AzureDeviceClient:
    return AzureDeviceClient()

@pytest.fixture
def system(device_controller: DeviceController, mock_interface: Interface, iot_device_client: AzureDeviceClient) -> System:
    system = System(device_controller, mock_interface, iot_device_client)
    system.is_collecting_readings = False
    return system


# @pytest.mark.asyncio
# async def test_loop_all_sensor_readings_logged_with_correct_units(system: System, logot: Logot):
#     system.is_collecting_readings = True
#     system.sleep_time = 0.1
#     try:
#         async with asyncio.TaskGroup() as tasks:
#             test_task = tasks.create_task(system.loop())            
#             await logot.await_for(logged.info("%s%f%sRH%s"), timeout=0.2)
#             await logot.await_for(logged.info("%s%f%s°C%s"), timeout=0.2)           
#             test_task.cancel()
#     except ExceptionGroup as eg:
#         raise AssertionError(f"{eg.exceptions}") from None


@pytest.mark.asyncio
async def test_loop_f1_press_turns_fan_on(mocker, system, fan_actuator):
    mock_response = {"value": 1, "key": "F1"}
    mocker.patch.object(MockInterface, "mock_event", AsyncMock(return_value=mock_response))
    fan_actuator.device.value = 0
    await system.loop()
    assert fan_actuator.device.value == 1


@pytest.mark.asyncio
async def test_loop_f1_release_turns_fan_off(mocker, system, fan_actuator):
    mock_response = {"value": 0, "key": "F1"}
    mocker.patch.object(MockInterface, "mock_event", AsyncMock(return_value=mock_response))
    fan_actuator.device.value = 1
    await system.loop()
    assert fan_actuator.device.value == 0


@pytest.mark.asyncio
async def test_loop_f2_press_turns_led_on(mocker, system, led_toggle_actuator):
    mock_response = {"value": 1, "key": "F2"}
    mocker.patch.object(MockInterface, "mock_event", AsyncMock(return_value=mock_response))
    led_toggle_actuator.device.value = 0
    await system.loop()
    assert led_toggle_actuator.device.value == 1


@pytest.mark.asyncio
async def test_loop_f2_releases_turns_led_off(mocker, system, led_toggle_actuator):
    mock_response = {"value": 0, "key": "F2"}
    mocker.patch.object(MockInterface, "mock_event", AsyncMock(return_value=mock_response))
    led_toggle_actuator.device.value = 1
    await system.loop()
    assert led_toggle_actuator.device.value == 0


@pytest.mark.asyncio
async def test_loop_f3_release_turns_led_off(mocker, system, led_toggle_actuator):
    mock_response = {"value": 0, "key": "F3"}
    mocker.patch.object(MockInterface, "mock_event", AsyncMock(return_value=mock_response))
    led_toggle_actuator.device.value = 1
    await system.loop()
    assert led_toggle_actuator.device.value == 0
