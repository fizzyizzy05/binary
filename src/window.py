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
from .bindec import *
from .hexcalc import *

@Gtk.Template(resource_path='/io/github/fizzyizzy05/binary/window.ui')
class BinaryWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'BinaryWindow'

    outLbl = Gtk.Template.Child() # output label
    bitLbl = Gtk.Template.Child() # bit counter label
    overlay = Gtk.Template.Child() # toast overlay
    entry = Gtk.Template.Child() # user input
    inDropdown = Gtk.Template.Child()
    outDropdown = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.outDropdown.set_selected(1) # Set the output to decimal by default

    toastTimeout = 1

    # Toast to tell the user decimal only numeric values
    decCharToast = Adw.Toast(
        title="Decimal only accepts the digits 0-9",
        timeout=toastTimeout,
    )
    # Toast to tell the user binary only accepts 0 or 1 digits
    binCharToast = Adw.Toast(
        title="Binary only accepts the digits 0 and 1",
        timeout=toastTimeout,
    )
    # Toast to tell the user binary only accepts 0 or 1 digits
    hexCharToast = Adw.Toast(
        title="Hexadecimal only accepts the digits 0-9 and A-F",
        timeout=toastTimeout,
    )
    # Toast to tell the user input and output bases are the same
    sameToast = Adw.Toast(
        title="Input and output bases are the same",
        timeout=1.5,
    )

    @Gtk.Template.Callback()
    def swap(self, *kwargs):
        a = self.inDropdown.get_selected()
        b = self.outDropdown.get_selected()
        self.inDropdown.set_selected(b)
        self.outDropdown.set_selected(a)

        if self.entry.get_text() != "":
            self.entry.set_text(self.outLbl.get_text())

    @Gtk.Template.Callback()
    def inputHandler(self, *kwargs):
        # 0 = Binary
        # 1 = Decimal
        # 2 = Hexadecimal
        # Binary to Decimal
        if self.inDropdown.get_selected() == 0 and self.outDropdown.get_selected() == 1:
            inStr = self.entry.get_text()
            if inStr != "":
                ans = bin2dec(inStr)
                if ans == "char":
                    self.overlay.add_toast(self.binCharToast)
                    return
                else:
                    # Set the output label and bit counter label
                    bits = bitCount(inStr)
                    self.outLbl.set_text(f"{ans}")
                    self.bitLbl.set_text(f"Bits: {bits} ({len(inStr)} bits)")
            else:
                self.blank()
        # Decimal to Binary
        elif self.inDropdown.get_selected() == 1 and self.outDropdown.get_selected() == 0:
            inStr = self.entry.get_text()
            if inStr != "":
                ans = dec2bin(inStr)
                if ans == "char":
                    self.overlay.add_toast(self.decCharToast)
                    return
                else:
                    bits = bitCount(ans)
                    self.bitLbl.set_text(f"Bits: {bits} ({len(ans)} bits)")
                    self.outLbl.set_text(ans)
            else:
                self.blank()
        # Decimal to Hexadecimal
        elif self.inDropdown.get_selected() == 1 and self.outDropdown.get_selected() == 2:
            inStr = self.entry.get_text()
            if inStr != "":
                ans = dec2hex(inStr)
                if ans == "char":
                    self.overlay.add_toast(self.decCharToast)
                    return
                else:
                    self.bitLbl.set_visible(False)
                    self.outLbl.set_text(ans)
            else:
                self.blank()
        # Hexadecimal to Decimal
        elif self.inDropdown.get_selected() == 2 and self.outDropdown.get_selected() == 1:
            inStr = self.entry.get_text()
            if inStr != "":
                ans = hex2dec(inStr)
                if ans == "char":
                    self.overlay.add_toast(self.hexCharToast)
                    return
                else:
                    self.bitLbl.set_visible(False)
                    self.outLbl.set_text(ans)
            else:
                self.blank()
        # Hexadecimal to Binary
        elif self.inDropdown.get_selected() == 2 and self.outDropdown.get_selected() == 0:
            inStr = self.entry.get_text()
            if inStr != "":
                ans = hex2bin(inStr)
                if ans == "char":
                    self.overlay.add_toast(self.hexCharToast)
                    return
                else:
                    bits = bitCount(ans)
                    self.bitLbl.set_text(f"Bits: {bits} ({len(ans)} bits)")
                    self.outLbl.set_text(ans)
            else:
                self.blank()
        # Binary to Hexadecimal
        elif self.inDropdown.get_selected() == 0 and self.outDropdown.get_selected() == 2:
            inStr = self.entry.get_text()
            if inStr != "":
                ans = bin2hex(inStr)
                if ans == "char":
                    self.overlay.add_toast(self.binCharToast)
                    return
                else:
                    bits = bitCount(inStr)
                    self.bitLbl.set_text(f"Bits: {bits} ({len(inStr)} bits)")
                    self.outLbl.set_text(ans)
            else:
                self.blank()
        # Same number bases
        elif self.inDropdown.get_selected() == self.outDropdown.get_selected():
            # Toast to tell the user they are converting between the same number format
            self.overlay.add_toast(self.sameToast)
            return

    def blank(self, *kwargs):
        # Return the label to it's original content. Using a function for this ensures it's always the same value, and makes it more consistent.
        self.bitLbl.set_visible(True)
        self.outLbl.set_text("0")
        self.bitLbl.set_text("Bits: none")
