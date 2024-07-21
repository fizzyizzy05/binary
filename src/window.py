# window.py
#
# Copyright 2023 Izzy Jackson
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

from gi.repository import Adw
from gi.repository import Gtk
from gi.repository import Gdk
import math

# Scripts used to calculate numbers
from .bitCount import *

@Gtk.Template(resource_path='/io/github/fizzyizzy05/binary/window.ui')
class BinaryWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'BinaryWindow'

    input_bits = Gtk.Template.Child() # individual bits in input bits dropdown
    output_bits = Gtk.Template.Child() # individual bits in output bits dropdown
    in_bit_label = Gtk.Template.Child() # input bit counter label
    out_bit_label = Gtk.Template.Child() # input bit counter label
    input_entry = Gtk.Template.Child() # user input
    output_entry = Gtk.Template.Child() # output label
    in_dropdown = Gtk.Template.Child()
    out_dropdown = Gtk.Template.Child()

    bits_text = _("bits") # String for the word Bits, makes translation easier.

    bases = Gtk.StringList.new(None)
    bases.append("Binary")
    bases.append("Decimal")
    bases.append("Hexadecimal")
    bases.append("Octal")

    editable = False

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.in_dropdown.set_model(self.bases)
        self.out_dropdown.set_model(self.bases)
        self.out_dropdown.set_selected(1) # Set the output to decimal by default
        self.input_entry.grab_focus()
        self.blank()

    @Gtk.Template.Callback()
    def change_input_base(self, *kwargs):
        try:
            self.output_handler()
            self.toggle_bit_counter()
        except:
            return

    @Gtk.Template.Callback()
    def change_output_base(self, *kwargs):
        try:
            self.input_handler()
            self.toggle_bit_counter()
        except:
            return

    @Gtk.Template.Callback()
    def input_handler(self, *kwargs):
        self.editable = False;
        in_str = self.input_entry.get_text()
        for char in in_str:
            if char.islower():
                self.input_entry.set_text(in_str.upper())
                self.input_entry.set_position(-1)
                return
        if in_str != "":
            ans = self.get_answer(input=in_str, in_base=self.in_dropdown.get_selected(), out_base=self.out_dropdown.get_selected())
            if ans == "char":
                self.input_entry.add_css_class("error")
                self.input_entry.set_tooltip_text("Invalid input")
                self.output_entry.set_tooltip_text(None)
            elif ans == "char_dual":
                self.input_entry.add_css_class("error")
                self.input_entry.set_tooltip_text("Invalid input")
                self.output_entry.add_css_class("error")
                self.output_entry.set_tooltip_text("Invalid input")
                self.output_entry.set_text(in_str)
            else:
                self.output_entry.set_text(ans)
                self.input_entry.remove_css_class("error")
                self.output_entry.set_tooltip_text(None)
        else:
            self.blank()
        self.toggle_mono()
        self.editable = True

    @Gtk.Template.Callback()
    def output_handler(self, *kwargs):
        if self.editable == True:
            in_str = self.output_entry.get_text()
            if in_str != "":
                in_base = self.out_dropdown.get_selected()
                out_base = self.in_dropdown.get_selected()
                ans = self.get_answer(input=in_str, in_base=in_base, out_base=out_base)
                if ans == "char":
                    self.output_entry.add_css_class("error")
                    self.input_entry.remove_css_class("error")
                    self.output_entry.set_tooltip_text("Invalid input")
                    self.input_entry.set_tooltip_text(None)
                elif ans == "char_dual":
                    self.input_entry.add_css_class("error")
                    self.input_entry.set_tooltip_text("Invalid input")
                    self.output_entry.add_css_class("error")
                    self.output_entry.set_tooltip_text("Invalid input")
                    self.input_entry.set_text(in_str)
                else:
                    self.input_entry.set_text(ans)
                    self.output_entry.remove_css_class("error")
                    self.input_entry.set_tooltip_text(None)
                self.output_entry.set_position(-1)
            else:
                self.blank()
            self.toggle_mono()
            self.editable = True

    def get_answer(self, *kwargs, input, in_base, out_base):
        # 0 = Binary
        # 1 = Decimal
        # 2 = Hexadecimal
        # 3 = Octal
        # No input
        # Binary to Decimal
        if in_base == 0 and out_base == 1:
            try:
                int(input, 2)
            except:
                self.clean_input_entry()
                return "char"
            ans = int(input, 2)
            # Set the output label and bit counter label
            bits = bitCount(input)
            self.update_input_bits(bits=bitCount(input), count=len(input))
            self.is_zero()
            return str(int(input, 2))
        # Decimal to Binary
        elif in_base == 1 and out_base == 0:
            try:
                int(input, 10)
            except:
                self.clean_input_entry()
                return "char"
            ans = bin(int(input)).lstrip("0b")
            self.update_output_bits(bits=bitCount(ans), count=len(ans))
            self.is_zero()
            return ans
        # Decimal to Hexadecimal
        elif in_base == 1 and out_base == 2:
            inStr = self.input_entry.get_text()
            try:
                int(inStr)
            except:
                self.clean_input_entry()
                return "char"
            ans = hex(int(inStr)).lstrip("0x").upper()
            self.is_zero()
            return ans
        # Hexadecimal to Decimal
        elif in_base == 2 and out_base == 1:
            try:
                int(input, 16)
            except:
                self.clean_input_entry()
                return "char"
            ans = str(int(input, 16))
            self.is_zero()
            return ans
        # Hexadecimal to Binary
        elif in_base == 2 and out_base == 0:
            try:
                int(input, 16)
            except:
                self.clean_input_entry()
                return "char"
            ans = bin(int(input, 16)).lstrip("0b")
            self.update_output_bits(bits=bitCount(ans), count=len(ans))
            self.is_zero()
            return ans
        # Binary to Hexadecimal
        elif in_base == 0 and out_base == 2:
            try:
                int(input, 2)
            except:
                self.clean_input_entry()
                return "char"
            ans = hex(int(input, 2)).strip("0x").upper()
            self.update_input_bits(bits=bitCount(input), count=len(input))
            self.is_zero()
            return ans
        # Oct to Bin
        elif in_base == 3 and out_base == 0:
            for char in str(input):
                try:
                    int(char, 8)
                except:
                    self.clean_input_entry()
                    return "char"
            ans = str(bin(int(input, 8)).lstrip("0b"))
            self.update_output_bits(bits=bitCount(ans), count=len(ans))
            return ans
        # Bin to Oct
        elif in_base == 0 and out_base == 3:
            try:
                int(input, 2)
            except:
                self.clean_input_entry()
                return "char"
            ans = str(oct(int(input, 2)).lstrip("0o"))
            self.update_input_bits(bits=bitCount(input), count=len(input))
            return ans
        # Oct to Dec
        elif in_base == 3 and out_base == 1:
            try:
                int(input, 8)
            except:
                self.clean_input_entry()
                return "char"
            ans = str(int(input, 8))
            return ans
        # Dec to Oct
        elif in_base == 1 and out_base == 3:
            try:
                int(input, 10)
            except:
                self.clean_input_entry()
                return "char"
            ans = str(oct(int(input)).lstrip("0o"))
            return ans
        # Oct to Hex
        elif in_base == 3 and out_base == 2:
            try:
                int(input, 8)
            except:
                self.clean_input_entry()
                return
            ans = hex(int(input, 8)).lstrip("0x").upper()
            return ans
        # Hex to Oct
        elif in_base == 2 and out_base == 3:
            try:
                int(input, 16)
            except:
                self.clean_input_entry()
                return "char"
            ans = oct(int(input, 16)).lstrip("0o")
            return ans
        # Same number bases
        elif in_base == out_base:
            # Set the output label to be the same as the input
            self.output_entry.add_css_class("mono")
            if in_base == 0:
                try:
                    int(input, 2)
                    return input
                except:
                    return "char_dual"
            elif self.in_dropdown.get_selected() == 1:
                try:
                    int(input, 10)
                    return input
                except:
                    return "char_dual"
            elif self.in_dropdown.get_selected() == 2:
                try:
                    int(input, 16)
                    return input
                except:
                    return "char_dual"
            elif self.in_dropdown.get_selected() == 3:
                try:
                    int(input, 8)
                    return input
                except:
                    return "char_dual"

    def is_zero(self, *kwargs):
        inStr = self.input_entry.get_text();
        for char in inStr:
            if char != '0':
                return
        self.input_entry.remove_css_class("error")
        self.output_entry.remove_css_class("error")
        self.blank()

    def blank(self, *kwargs):
        # Return the label to it's original content. Using a function for this ensures it's always the same value, and makes it more consistent.
        self.output_entry.set_text("")
        self.input_entry.set_text("")
        self.in_bit_label.set_label(f"0 {self.bits_text}")
        self.out_bit_label.set_label(f"0 {self.bits_text}")
        bit_counter_text = _("Enter a number to see its bits")
        self.input_bits.set_text(bit_counter_text)
        self.output_bits.set_text(bit_counter_text)
        self.toggle_mono()
        self.input_entry.remove_css_class("error")
        self.output_entry.remove_css_class("error")

    def clean_input_entry(self, *kwargs):
        self.input_entry.add_css_class("error")

    def update_input_bits(self, *kwargs, bits, count):
        self.in_bit_label.set_label(f"{count} {self.bits_text}")
        self.input_bits.set_label(f"{bits}")

    def update_output_bits(self, *kwargs, bits, count):
        self.out_bit_label.set_label(f"{count} {self.bits_text}")
        self.output_bits.set_label(f"{bits}")

    def toggle_mono(self, *kwargs):
        if self.input_entry.get_text() != "":
            self.input_entry.add_css_class("mono")
        else:
            self.input_entry.remove_css_class("mono")

        if self.output_entry.get_text() != "":
            self.output_entry.add_css_class("mono")
        else:
            self.output_entry.remove_css_class("mono")

    def toggle_bit_counter(self, *kwargs):
        if self.out_dropdown.get_selected() == 0 and self.in_dropdown.get_selected() == 0:
            self.in_bit_label.set_visible(True)
            self.out_bit_label.set_visible(True)
        elif self.in_dropdown.get_selected() == 0:
            self.in_bit_label.set_visible(True)
            self.out_bit_label.set_visible(False)
        elif self.out_dropdown.get_selected() == 0:
            self.in_bit_label.set_visible(False)
            self.out_bit_label.set_visible(True)
        else:
            self.in_bit_label.set_visible(False)
            self.out_bit_label.set_visible(False)
