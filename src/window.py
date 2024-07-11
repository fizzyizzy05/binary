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

    bitsTxt = _("bits") # String for the word Bits, makes translation easier.

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
    def change_bases(self, *kwargs):
        try:
            self.input_handler()

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
        except:
            return

    @Gtk.Template.Callback()
    def input_handler(self, *kwargs):
        self.editable = False;
        in_str = self.input_entry.get_text()
        if in_str != "":
            ans = self.get_answer(input=in_str, in_base=self.in_dropdown.get_selected(), out_base=self.out_dropdown.get_selected())
            if ans != "char":
                self.output_entry.set_text(ans)
        else:
            self.blank()
            self.input_entry.remove_css_class("error")
            self.input_entry.remove_css_class("mono")
            self.output_entry.remove_css_class("error")
            self.output_entry.remove_css_class("mono")
            empty_counter_text = _("Enter a number to see its bits")
            self.input_bits.set_text(empty_counter_text)
            self.output_bits.set_text(empty_counter_text)
        self.editable = True

    @Gtk.Template.Callback()
    def output_handler(self, *kwargs):
        if self.editable == True:
            in_str = self.output_entry.get_text()
            print(in_str)
            if in_str == "":
                self.blank()
                self.input_entry.remove_css_class("error")
                self.input_entry.remove_css_class("mono")
                self.output_entry.remove_css_class("error")
                self.output_entry.remove_css_class("mono")
                empty_counter_text = _("Enter a number to see its bits")
                self.input_bits.set_text(empty_counter_text)
                self.output_bits.set_text(empty_counter_text)
            else:
                in_base = self.out_dropdown.get_selected()
                out_base = self.in_dropdown.get_selected()
                ans = self.get_answer(input=in_str, in_base=in_base, out_base=out_base)
                print(ans)
                if ans != "char":
                    self.input_entry.set_text(ans)
                    self.output_entry.set_position(len(ans))

            self.editable = True

    def get_answer(self, *kwargs, input, in_base, out_base):
        # 0 = Binary
        # 1 = Decimal
        # 2 = Hexadecimal
        # 3 = Octal
        # No input
        self.input_entry.add_css_class("mono")

        print (f"input: {in_base}")
        print (f"output: {out_base}")
        # Binary to Decimal
        if in_base == 0 and out_base == 1:
            try:
                int(input, 2)
                self.input_entry.remove_css_class("error")
                self.output_entry.add_css_class("mono")
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
                self.input_entry.remove_css_class("error")
                self.output_entry.add_css_class("mono")
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
                self.input_entry.remove_css_class("error")
                self.output_entry.add_css_class("mono")
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
                self.input_entry.remove_css_class("error")
                self.output_entry.add_css_class("mono")
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
                self.input_entry.remove_css_class("error")
                self.output_entry.add_css_class("mono")
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
                self.input_entry.remove_css_class("error")
                self.output_entry.add_css_class("mono")
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
                    self.input_entry.remove_css_class("error")
                    self.output_entry.add_css_class("mono")
                except:
                    self.clean_input_entry()
                    return "char"
            ans = str(bin(int(input, 8)).lstrip("0b"))
            self.update_output_bits(bits=bitCount(ans), count=len(ans))
            self.in_bit_label.set_visible(True)
            return ans
        # Bin to Oct
        elif in_base == 0 and out_base == 3:
            try:
                int(input, 2)
                self.input_entry.remove_css_class("error")
                self.output_entry.add_css_class("mono")
            except:
                self.clean_input_entry()
                return "char"
            ans = str(oct(int(input, 2)).lstrip("0o"))
            self.update_input_bits(bits=bitCount(input), count=len(input))
            self.in_bit_label.set_visible(True)
            return ans
        # Oct to Dec
        elif in_base == 3 and out_base == 1:
            try:
                int(input, 8)
                self.input_entry.remove_css_class("error")
                self.output_entry.add_css_class("mono")
            except:
                self.clean_input_entry()
                return "char"
            ans = str(int(input, 8))
            self.in_bit_label.set_visible(False)
            return ans
        # Dec to Oct
        elif in_base == 1 and out_base == 3:
            try:
                int(input, 10)
                self.input_entry.remove_css_class("error")
                self.output_entry.add_css_class("mono")
            except:
                self.clean_input_entry()
                return "char"
            ans = str(oct(int(input)).lstrip("0o"))
            self.in_bit_label.set_visible(False)
            return ans
        # Oct to Hex
        elif in_base == 3 and out_base == 2:
            try:
                int(input, 8)
                self.input_entry.remove_css_class("error")
                self.output_entry.add_css_class("mono")
            except:
                self.clean_input_entry()
                return
            ans = hex(int(input, 8)).lstrip("0x").upper()
            self.in_bit_label.set_visible(False)
            return ans
        # Hex to Oct
        elif in_base == 2 and out_base == 3:
            try:
                int(input, 16)
                self.input_entry.remove_css_class("error")
                self.output_entry.add_css_class("mono")
            except:
                self.clean_input_entry()
                return "char"
            ans = oct(int(input, 16)).lstrip("0o")
            self.in_bit_label.set_visible(False)
            return ans
        # Same number bases
        elif in_base == out_base:
            # Set the output label to be the same as the input
            self.output_entry.add_css_class("mono")
            if in_base == 0:
                try:
                    int(input, 2)
                    self.input_entry.remove_css_class("error")
                    self.output_entry.remove_css_class("error")
                    self.update_input_bits(bits=bitCount(input), count=len(input))
                    self.update_output_bits(bits=bitCount(input), count=len(input))
                except:
                    self.input_entry.add_css_class("error")
                    self.output_entry.add_css_class("error")
                self.in_bit_label.set_visible(True)
            elif self.in_dropdown.get_selected() == 1:
                self.in_bit_label.set_visible(False)
                try:
                    int(input, 10)
                    self.input_entry.remove_css_class("error")
                    self.output_entry.remove_css_class("error")
                except:
                    self.input_entry.add_css_class("error")
                    self.output_entry.add_css_class("error")
            elif self.in_dropdown.get_selected() == 2:
                self.in_bit_label.set_visible(False)
                try:
                    int(input, 16)
                    self.input_entry.remove_css_class("error")
                    self.output_entry.remove_css_class("error")
                except:
                    self.input_entry.add_css_class("error")
                    self.output_entry.add_css_class("error")
            elif self.in_dropdown.get_selected() == 3:
                self.in_bit_label.set_visible(False)
                try:
                    int(input, 8)
                    self.input_entry.remove_css_class("error")
                    self.output_entry.remove_css_class("error")
                except:
                    self.input_entry.add_css_class("error")
                    self.output_entry.add_css_class("error")
            return input

    def is_zero(self, *kwargs):
        inStr = self.input_entry.get_text();
        for char in inStr:
            if char != '0':
                return
        self.input_entry.remove_css_class("error")
        self.output_entry.remove_css_class("error")
        self.blank()

        if self.in_dropdown.get_selected() != 0 and self.out_dropdown.get_selected() != 0:
            self.in_bit_label.set_visible(False)

    def blank(self, *kwargs):
        # Return the label to it's original content. Using a function for this ensures it's always the same value, and makes it more consistent.
        self.in_bit_label.set_visible(True)
        self.output_entry.set_text("")
        self.input_entry.set_text("")
        self.in_bit_label.set_label(f"0 {self.bitsTxt}")
        self.out_bit_label.set_label(f"0 {self.bitsTxt}")

    def clean_input_entry(self, *kwargs):
        self.input_entry.add_css_class("error")

    def update_input_bits(self, *kwargs, bits, count):
        self.in_bit_label.set_label(f"{count} {self.bitsTxt}")
        self.input_bits.set_label(f"{bits}")

    def update_output_bits(self, *kwargs, bits, count):
        self.out_bit_label.set_label(f"{count} {self.bitsTxt}")
        self.output_bits.set_label(f"{bits}")
