# File: src/common/interfaces/reterminal.py
# Project: final-project-upstream
# Creation date: 29 Apr 2025
# Author: michaelhaaf <michael.haaf@gmail.com>
# Modified By: N/A
# Changes made: N/A
# -----
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

from abc import abstractmethod

from common.interfaces import Interface


class ReterminalInterface(Interface):
    """Implementation of the SystemInterface class for the Reterminal chassis."""

    def __init__(self) -> None:
        """Initialize the interface class."""
        import seeed_python_rpi.button as rt_btn
        import seeed_python_rpi.core as rt

        self.btn_definition = rt_btn
        self.btn_device = rt.get_button_device()  # pyright: ignore reportAttributeAccessIssue
        super().__init__()

    async def event_loop(self) -> None:
        """Runs an event loop that listens for reterminal button presses."""
        async for event in self.btn_device.async_read_loop():
            button_event = self.btn_definition.ButtonEvent(event)
            if button_event.name is not None and button_event.value == 1:
                self.key_press(button_event.name.name)
            elif button_event.name is not None and button_event.value == 0:
                self.key_release(button_event.name.name)

    def end_event_loop(self) -> None:
        """Terminates the event loop started by the event_loop method."""
        raise StopAsyncIteration

    @abstractmethod
    def key_press(self, key: str) -> None:
        """See base class."""
        pass

    @abstractmethod
    def key_release(self, key: str) -> None:
        """See base class."""
        pass
