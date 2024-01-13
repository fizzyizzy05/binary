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
        self.css_provider = Gtk.CssProvider()
        self.css_provider.load_from_resource('/io/github/fizzyizzy05/binary/window.css')
        Gtk.StyleContext.add_provider_for_display(Gdk.Display.get_default(), self.css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        super().__init__(**kwargs)
        self.outDropdown.set_selected(1) # Set the output to decimal by default

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
        if self.inDropdown.get_selected() == 0 and self.outDropdown.get_selected() == 1:
            inStr = self.entry.get_text()

            if inStr != "":
                ans = bin2dec(inStr)
                bits = bitCount(inStr)

                if ans == "char":
                    # Toast to tell the user binary only accepts 0 or 1 digits
                    wrongToast = Adw.Toast(
                        title="Binary only accepts the digits 0 and 1",
                        timeout=1.5,
                    )
                    self.overlay.add_toast(wrongToast)
                    return
                else:
                    # Set the output label and bit counter label
                    self.outLbl.set_text(f"{ans}")
                    self.bitLbl.set_text(f"Bits: {bits} ({len(inStr)} bits)")
            else:
                self.blank()

        elif self.inDropdown.get_selected() == 1 and self.outDropdown.get_selected() == 0:
            inStr = self.entry.get_text()

            if inStr != "":
                ans = dec2bin(inStr)
                bits = bitCount(ans)
                self.bitLbl.set_text(f"Bits: {bits} ({len(ans)} bits)")
                self.outLbl.set_text(ans)

            else:
                self.blank()

        elif self.inDropdown.get_selected() == self.outDropdown.get_selected():
            # Toast to tell the user they are converting between the same number format
            sameToast = Adw.Toast(
                title="Input and output bases are the same",
                timeout=1.5,
            )
            self.overlay.add_toast(sameToast)

    def blank(self, *kwargs):
        # Return the label to it's original content. Using a function for this ensures it's always the same value, and makes it more consistent.
        self.outLbl.set_text("0")
        self.bitLbl.set_text("Bits: none")
