# twos_compliment.py
#
# Copyright 2023-2024 Isabelle Jackson
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# SPDX-License-Identifier: GPL-3.0-or-later

# This script is auxiliary to get_answer.py, it converts answers to/from two's compliment first before calculating them in get_answer

from .get_answer import *

def twos_compliment(input, in_base, in_2c, out_base, out_2c):
    if in_2c == False and out_2c == True:
        i = get_answer(input, in_base, 2)
        print(i)
        ans = "1"
        for d in i:
            if d == '0':
                ans += "1"
            else:
                ans += "0"

        print(ans)

        ans = bin(int(ans, 2) + 1)
        return ans.removeprefix("0b")
