# File: src/water_floods_subsystem/__main__.py
# Project: final-project-refarminal
# Creation date: 29 Apr 2025
# Author: michaelhaaf <michael.haaf@gmail.com>
# Modified By: Madison Cassley
# Changes made: Removed things to keep base for my devices
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

import contextlib, sys
from pathlib import Path

if not __package__:
    sys.path.insert(0, Path(__file__).parent.parent.as_posix())

if __name__ == "__main__":
    from example_system.runner import main
    with contextlib.suppress(KeyboardInterrupt):
        main()
