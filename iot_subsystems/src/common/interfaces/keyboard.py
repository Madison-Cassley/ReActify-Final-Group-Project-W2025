# File: src/common/interfaces/keyboard.py
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
        await self.listen_keyboard(on_press=self.key_press, on_release=self.key_release)

    def end_event_loop(self) -> None:
        """See base class."""
        self.stop_listening()

    @abstractmethod
    def key_press(self, key: str) -> None:
        """See base class."""
        pass

    @abstractmethod
    def key_release(self, key: str) -> None:
        """See base class."""
        pass
