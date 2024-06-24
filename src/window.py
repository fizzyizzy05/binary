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

    bitsTxt = _("bits") # String for the word Bits, makes translation easier.

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.outDropdown.set_selected(1) # Set the output to decimal by default
        self.blank()

    # Toast to tell the user input and output bases are the same
    sameToast = Adw.Toast(
        title=_("Input and output bases are the same"),
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
        # 3 = Octal
        # Binary to Decimal
        if self.inDropdown.get_selected() == 0 and self.outDropdown.get_selected() == 1:
            inStr = self.entry.get_text()
            if inStr != "":
                try:
                    int(inStr, 2)
                    self.entry.remove_css_class("error")
                except:
                    self.cleanEntry()
                    return
                ans = int(inStr, 2)
                # Set the output label and bit counter label
                bits = bitCount(inStr)
                self.outLbl.set_text(str(int(inStr, 2)))
                self.updateBits(bits=bitCount(inStr), count=len(inStr))
                self.isZero()
            else:
                self.blank()
                self.entry.remove_css_class("error")
        # Decimal to Binary
        elif self.inDropdown.get_selected() == 1 and self.outDropdown.get_selected() == 0:
            inStr = self.entry.get_text()
            if inStr != "":
                try:
                    int(inStr, 10)
                    self.entry.remove_css_class("error")
                except:
                    self.cleanEntry()
                    return
                ans = bin(int(inStr)).lstrip("0b")
                self.updateBits(bits=bitCount(ans), count=len(ans))
                self.outLbl.set_text(ans)
                self.isZero()
            else:
                self.blank()
                self.entry.remove_css_class("error")
        # Decimal to Hexadecimal
        elif self.inDropdown.get_selected() == 1 and self.outDropdown.get_selected() == 2:
            inStr = self.entry.get_text()
            if inStr != "":
                try:
                    int(inStr)
                    self.entry.remove_css_class("error")
                except:
                    self.cleanEntry()
                    return
                ans = hex(int(inStr)).lstrip("0x").upper()
                self.bitLbl.set_visible(False)
                self.outLbl.set_text(ans)
                self.isZero()
            else:
                self.blank()
                self.entry.remove_css_class("error")
        # Hexadecimal to Decimal
        elif self.inDropdown.get_selected() == 2 and self.outDropdown.get_selected() == 1:
            inStr = self.entry.get_text().upper()
            if inStr != "":
                try:
                    int(inStr, 16)
                    self.entry.remove_css_class("error")
                except:
                    self.cleanEntry()
                    return
                ans = int(inStr, 16)
                self.bitLbl.set_visible(False)
                self.outLbl.set_text(str(int(inStr, 16)))
                self.isZero()
            else:
                self.blank()
                self.entry.remove_css_class("error")
        # Hexadecimal to Binary
        elif self.inDropdown.get_selected() == 2 and self.outDropdown.get_selected() == 0:
            inStr = self.entry.get_text().upper()
            if inStr != "":
                try:
                    int(inStr, 16)
                    self.entry.remove_css_class("error")
                except:
                    self.cleanEntry()
                    return
                ans = bin(int(inStr, 16)).lstrip("0b")
                self.updateBits(bits=bitCount(ans), count=len(ans))
                self.outLbl.set_text(ans)
                self.isZero()
            else:
                self.blank()
                self.entry.remove_css_class("error")
        # Binary to Hexadecimal
        elif self.inDropdown.get_selected() == 0 and self.outDropdown.get_selected() == 2:
            inStr = self.entry.get_text()
            if inStr != "":
                try:
                    int(inStr, 2)
                    self.entry.remove_css_class("error")
                except:
                    self.cleanEntry()
                    return
                ans = hex(int(inStr, 2)).strip("0x").upper()
                self.updateBits(bits=bitCount(inStr), count=len(inStr))
                self.outLbl.set_text(ans)
                self.isZero()
            else:
                self.blank()
                self.entry.remove_css_class("error")
        # Oct to Bin
        elif self.inDropdown.get_selected() == 3 and self.outDropdown.get_selected() == 0:
            inStr = self.entry.get_text()
            if inStr != "":
                for char in str(inStr):
                    try:
                        int(char, 8)
                        self.entry.remove_css_class("error")
                    except:
                        self.cleanEntry()
                        return
                ans = bin(int(inStr, 8)).lstrip("0b")
                self.outLbl.set_text(ans)
                self.updateBits(bits=bitCount(ans), count=len(ans))
            else:
                self.blank()
                self.entry.remove_css_class("error")
        # Bin to Oct
        elif self.inDropdown.get_selected() == 0 and self.outDropdown.get_selected() == 3:
            inStr = self.entry.get_text()
            if inStr != "":
                try:
                    int(inStr, 2)
                    self.entry.remove_css_class("error")
                except:
                    self.cleanEntry()
                    return
                ans = oct(int(inStr, 2)).lstrip("0o")
                self.outLbl.set_text(ans)
                self.updateBits(bits=bitCount(inStr), count=len(inStr))
            else:
                self.blank()
                self.entry.remove_css_class("error")
        # Oct to Dec
        elif self.inDropdown.get_selected() == 3 and self.outDropdown.get_selected() == 1:
            inStr = self.entry.get_text()
            if inStr != "":
                try:
                    int(inStr, 8)
                    self.entry.remove_css_class("error")
                except:
                    self.cleanEntry()
                    return
                ans = int(inStr, 8)
                self.outLbl.set_text(str(ans))
                self.bitLbl.set_visible(False)
            else:
                self.blank()
                self.entry.remove_css_class("error")
        # Dec to Oct
        elif self.inDropdown.get_selected() == 1 and self.outDropdown.get_selected() == 3:
            inStr = self.entry.get_text()
            if inStr != "":
                try:
                    int(inStr, 10)
                    self.entry.remove_css_class("error")
                except:
                    self.cleanEntry()
                    return
                ans = oct(int(inStr)).lstrip("0o")
                self.outLbl.set_text(str(ans))
                self.bitLbl.set_visible(False)
            else:
                self.blank()
                self.entry.remove_css_class("error")
        # Oct to Hex
        elif self.inDropdown.get_selected() == 3 and self.outDropdown.get_selected() == 2:
            inStr = self.entry.get_text()
            if inStr != "":
                try:
                    int(inStr, 8)
                    self.entry.remove_css_class("error")
                except:
                    self.overlay.add_toast(self.hexCharToast)
                    self.cleanEntry()
                    return
                ans = hex(int(inStr, 8)).lstrip("0x").upper()
                self.outLbl.set_text(ans)
                self.bitLbl.set_visible(False)
            else:
                self.blank()
                self.entry.remove_css_class("error")
        # Hex to Oct
        elif self.inDropdown.get_selected() == 2 and self.outDropdown.get_selected() == 3:
            inStr = self.entry.get_text()
            if inStr != "":
                try:
                    int(inStr, 16)
                    self.entry.remove_css_class("error")
                except:
                    self.overlay.add_toast(self.hexCharToast)
                    self.cleanEntry()
                    return
                ans = oct(int(inStr, 16)).lstrip("0o")
                self.outLbl.set_text(str(ans))
                self.bitLbl.set_visible(False)
            else:
                self.blank()
                self.entry.remove_css_class("error")
        # Same number bases
        elif self.inDropdown.get_selected() == self.outDropdown.get_selected():
            # Toast to tell the user they are converting between the same number format
            self.overlay.add_toast(self.sameToast)
            self.entry.get_buffer().set_text("", -1)
            self.blank()
            return

    def isZero(self, *kwargs):
        inStr = self.entry.get_text();
        for char in inStr:
            if char != '0':
                return
        self.entry.remove_css_class("error")
        self.outLbl.set_text("0")
        self.blank()

        if self.inDropdown.get_selected() != 0 and self.outDropdown.get_selected() != 0:
            self.bitLbl.set_visible(False)

    def blank(self, *kwargs):
        # Return the label to it's original content. Using a function for this ensures it's always the same value, and makes it more consistent.
        self.bitLbl.set_visible(True)
        self.outLbl.set_text("0")
        self.bitLbl.set_text(f"0 {self.bitsTxt}")

    def cleanEntry(self, *kwargs):
        self.entry.add_css_class("error")

    def updateBits(self, *kwargs, bits, count):
        self.bitLbl.set_text(f"{count} {self.bitsTxt}: {bits}")
