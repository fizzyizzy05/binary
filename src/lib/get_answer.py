# get_answer.py
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

# This script returns the answer of a calculation to the main window.
def calc_numerator(input, in_base, out_base):
    # Convert the input to base 10
    input_dec = int(input, in_base)
    
    # Convert input_dec to a list of the digits in decimal
    output_list = []

    if input_dec == 0:
        return "0"

    while input_dec:
        output_list += [int(input_dec % out_base)]
        input_dec //= out_base
        
    output_list = output_list[::-1]

    # Convert the decimals in the list greater than 9 to letters
    # This works upto Z = 35.
    for i in range(len(output_list)):
        if output_list[i] > 9:
            output_list[i] = chr(output_list[i] + 55) # A = 65, and we start from 10.

    return "".join(map(str, output_list))

def get_answer(input, in_base, out_base):
    split_input = input.split('.')
    print(len(split_input))
    # space characters count as invalid input
    if (" " in input):
        return "char"

    if '+' in input:
        split_input('')

    for x in split_input:
        # Check if the input is valid for in_base, where in_base is between 2 and 36 inclusive.
        # Bases above 36 are not universally standard, so we assume they are invalid.
        try:
            int(x, in_base)
        except:
            return "char"

    # Same number bases
    if in_base == out_base:
        # Set the output label to be the same as the input
        try:
            int(x, in_base)
            return input
        except:
            return "char_dual"

    if len(split_input) == 1:
        return calc_numerator(split_input[0], in_base, out_base)
    if len(split_input) == 2 and split_input[1] == 0:
        # TODO: add separate calculations
        return f"{calc_numerator(split_input[0], in_base, out_base)}.0"
    else:
        return "char"
