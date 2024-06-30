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

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.in_dropdown.set_model(self.bases)
        self.out_dropdown.set_model(self.bases)
        self.out_dropdown.set_selected(1) # Set the output to decimal by default
        self.input_entry.grab_focus()
        self.blank()

    @Gtk.Template.Callback()
    def changeBases(self, *kwargs):
        try:
            self.inputHandler()

            if self.in_dropdown.get_selected() == 0:
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
    def swap(self, *kwargs):
        inVal = self.input_entry.get_text()
        outVal = self.output_entry.get_text()
        inBase = self.in_dropdown.get_selected()
        outBase = self.out_dropdown.get_selected()
        self.in_dropdown.set_selected(outBase)
        self.out_dropdown.set_selected(inBase)

        if self.input_entry.get_text() != "":
            self.input_entry.set_text(outVal)
            self.output_entry.set_text(inVal)

    @Gtk.Template.Callback()
    def inputHandler(self, *kwargs):
        # 0 = Binary
        # 1 = Decimal
        # 2 = Hexadecimal
        # 3 = Octal
        # No input
        if self.input_entry.get_text() == "":
            self.blank()
            self.input_entry.remove_css_class("error")
            self.input_entry.remove_css_class("mono")
            self.output_entry.remove_css_class("error")
            self.output_entry.remove_css_class("mono")
            empty_counter_text = _("Enter a number to see its bits")
            self.input_bits.set_text(empty_counter_text)
            self.output_bits.set_text(empty_counter_text)
        else:
            self.input_entry.add_css_class("mono")
            # Binary to Decimal
            if self.in_dropdown.get_selected() == 0 and self.out_dropdown.get_selected() == 1:
                inStr = self.input_entry.get_text()
                try:
                    int(inStr, 2)
                    self.input_entry.remove_css_class("error")
                    self.output_entry.add_css_class("mono")
                except:
                    self.cleaninput_entry()
                    return
                ans = int(inStr, 2)
                # Set the output label and bit counter label
                bits = bitCount(inStr)
                self.output_entry.set_text(str(int(inStr, 2)))
                self.update_input_bits(bits=bitCount(inStr), count=len(inStr))
                self.isZero()
            # Decimal to Binary
            elif self.in_dropdown.get_selected() == 1 and self.out_dropdown.get_selected() == 0:
                inStr = self.input_entry.get_text()
                try:
                    int(inStr, 10)
                    self.input_entry.remove_css_class("error")
                    self.output_entry.add_css_class("mono")
                except:
                    self.cleaninput_entry()
                    return
                ans = bin(int(inStr)).lstrip("0b")
                self.update_output_bits(bits=bitCount(ans), count=len(ans))
                self.output_entry.set_text(ans)
                self.isZero()
            # Decimal to Hexadecimal
            elif self.in_dropdown.get_selected() == 1 and self.out_dropdown.get_selected() == 2:
                inStr = self.input_entry.get_text()
                try:
                    int(inStr)
                    self.input_entry.remove_css_class("error")
                    self.output_entry.add_css_class("mono")
                except:
                    self.cleaninput_entry()
                    return
                ans = hex(int(inStr)).lstrip("0x").upper()
                self.output_entry.set_text(ans)
                self.isZero()
            # Hexadecimal to Decimal
            elif self.in_dropdown.get_selected() == 2 and self.out_dropdown.get_selected() == 1:
                inStr = self.input_entry.get_text().upper()
                try:
                    int(inStr, 16)
                    self.input_entry.remove_css_class("error")
                    self.output_entry.add_css_class("mono")
                except:
                    self.cleaninput_entry()
                    return
                ans = int(inStr, 16)
                self.output_entry.set_text(str(int(inStr, 16)))
                self.isZero()
            # Hexadecimal to Binary
            elif self.in_dropdown.get_selected() == 2 and self.out_dropdown.get_selected() == 0:
                inStr = self.input_entry.get_text().upper()
                try:
                    int(inStr, 16)
                    self.input_entry.remove_css_class("error")
                    self.output_entry.add_css_class("mono")
                except:
                    self.cleaninput_entry()
                    return
                ans = bin(int(inStr, 16)).lstrip("0b")
                self.update_output_bits(bits=bitCount(ans), count=len(ans))
                self.output_entry.set_text(ans)
                self.isZero()
            # Binary to Hexadecimal
            elif self.in_dropdown.get_selected() == 0 and self.out_dropdown.get_selected() == 2:
                inStr = self.input_entry.get_text()
                try:
                    int(inStr, 2)
                    self.input_entry.remove_css_class("error")
                    self.output_entry.add_css_class("mono")
                except:
                    self.cleaninput_entry()
                    return
                ans = hex(int(inStr, 2)).strip("0x").upper()
                self.update_input_bits(bits=bitCount(inStr), count=len(inStr))
                self.output_entry.set_text(ans)
                self.isZero()
            # Oct to Bin
            elif self.in_dropdown.get_selected() == 3 and self.out_dropdown.get_selected() == 0:
                inStr = self.input_entry.get_text()
                for char in str(inStr):
                    try:
                        int(char, 8)
                        self.input_entry.remove_css_class("error")
                        self.output_entry.add_css_class("mono")
                    except:
                        self.cleaninput_entry()
                        return
                ans = bin(int(inStr, 8)).lstrip("0b")
                self.output_entry.set_text(ans)
                self.update_output_bits(bits=bitCount(ans), count=len(ans))
                self.in_bit_label.set_visible(True)
            # Bin to Oct
            elif self.in_dropdown.get_selected() == 0 and self.out_dropdown.get_selected() == 3:
                inStr = self.input_entry.get_text()
                try:
                    int(inStr, 2)
                    self.input_entry.remove_css_class("error")
                    self.output_entry.add_css_class("mono")
                except:
                    self.cleaninput_entry()
                    return
                ans = oct(int(inStr, 2)).lstrip("0o")
                self.output_entry.set_text(ans)
                self.update_input_bits(bits=bitCount(inStr), count=len(inStr))
                self.in_bit_label.set_visible(True)
            # Oct to Dec
            elif self.in_dropdown.get_selected() == 3 and self.out_dropdown.get_selected() == 1:
                inStr = self.input_entry.get_text()
                try:
                    int(inStr, 8)
                    self.input_entry.remove_css_class("error")
                    self.output_entry.add_css_class("mono")
                except:
                    self.cleaninput_entry()
                    return
                ans = int(inStr, 8)
                self.output_entry.set_text(str(ans))
                self.in_bit_label.set_visible(False)
            # Dec to Oct
            elif self.in_dropdown.get_selected() == 1 and self.out_dropdown.get_selected() == 3:
                inStr = self.input_entry.get_text()
                try:
                    int(inStr, 10)
                    self.input_entry.remove_css_class("error")
                    self.output_entry.add_css_class("mono")
                except:
                    self.cleaninput_entry()
                    return
                ans = oct(int(inStr)).lstrip("0o")
                self.output_entry.set_text(str(ans))
                self.in_bit_label.set_visible(False)
            # Oct to Hex
            elif self.in_dropdown.get_selected() == 3 and self.out_dropdown.get_selected() == 2:
                inStr = self.input_entry.get_text()
                try:
                    int(inStr, 8)
                    self.input_entry.remove_css_class("error")
                    self.output_entry.add_css_class("mono")
                except:
                    self.cleaninput_entry()
                    return
                ans = hex(int(inStr, 8)).lstrip("0x").upper()
                self.output_entry.set_text(ans)
                self.in_bit_label.set_visible(False)
            # Hex to Oct
            elif self.in_dropdown.get_selected() == 2 and self.out_dropdown.get_selected() == 3:
                inStr = self.input_entry.get_text()
                try:
                    int(inStr, 16)
                    self.input_entry.remove_css_class("error")
                    self.output_entry.add_css_class("mono")
                except:
                    self.cleaninput_entry()
                    return
                ans = oct(int(inStr, 16)).lstrip("0o")
                self.output_entry.set_text(str(ans))
                self.in_bit_label.set_visible(False)
            # Same number bases
            elif self.in_dropdown.get_selected() == self.out_dropdown.get_selected():
                inStr = self.input_entry.get_text()
                # Set the output label to be the same as the input
                self.output_entry.set_text(self.input_entry.get_text())
                self.output_entry.add_css_class("mono")
                if self.in_dropdown.get_selected() == 0:
                    try:
                        int(inStr, 2)
                        self.input_entry.remove_css_class("error")
                        self.output_entry.remove_css_class("error")
                        self.update_input_bits(bits=bitCount(inStr), count=len(inStr))
                        self.update_output_bits(bits=bitCount(inStr), count=len(inStr))
                    except:
                        self.input_entry.add_css_class("error")
                        self.output_entry.add_css_class("error")
                    self.in_bit_label.set_visible(True)
                elif self.in_dropdown.get_selected() == 1:
                    self.in_bit_label.set_visible(False)
                    try:
                        int(inStr, 10)
                        self.input_entry.remove_css_class("error")
                        self.output_entry.remove_css_class("error")
                    except:
                        self.input_entry.add_css_class("error")
                        self.output_entry.add_css_class("error")
                elif self.in_dropdown.get_selected() == 2:
                    self.in_bit_label.set_visible(False)
                    try:
                        int(inStr, 16)
                        self.input_entry.remove_css_class("error")
                        self.output_entry.remove_css_class("error")
                    except:
                        self.input_entry.add_css_class("error")
                        self.output_entry.add_css_class("error")
                elif self.in_dropdown.get_selected() == 3:
                    self.in_bit_label.set_visible(False)
                    try:
                        int(inStr, 8)
                        self.input_entry.remove_css_class("error")
                        self.output_entry.remove_css_class("error")
                    except:
                        self.input_entry.add_css_class("error")
                        self.output_entry.add_css_class("error")

    def isZero(self, *kwargs):
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
        self.in_bit_label.set_label(f"0 {self.bitsTxt}")
        self.out_bit_label.set_label(f"0 {self.bitsTxt}")

    def cleaninput_entry(self, *kwargs):
        self.input_entry.add_css_class("error")

    def update_input_bits(self, *kwargs, bits, count):
        self.in_bit_label.set_label(f"{count} {self.bitsTxt}")
        self.input_bits.set_label(f"{bits}")

    def update_output_bits(self, *kwargs, bits, count):
        self.out_bit_label.set_label(f"{count} {self.bitsTxt}")
        self.output_bits.set_label(f"{bits}")
