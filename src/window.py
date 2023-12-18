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
    def inputHandler(self, *kwargs):
        if self.inDropdown.get_selected() == 0 and self.outDropdown.get_selected() == 1:
            self.bin2dec()
        elif self.inDropdown.get_selected() == 1 and self.outDropdown.get_selected() == 0:
            self.dec2bin()
        elif self.inDropdown.get_selected() == self.outDropdown.get_selected():
            # Toast to tell they are converting between the same number format
            sameToast = Adw.Toast(
                title="Converting to the same number format",
                timeout=1.5,
            )
            self.overlay.add_toast(sameToast)

    def bin2dec(self, *kwargs):
        inStr = self.entry.get_text()

        if inStr != "":
            ans = 0
            mult = 1
            bits = []

            # Work out how many bits the binary input is, and work out the largest bits value
            for count in range(len(inStr) - 1):
                mult = mult * 2

            # Check each bit in the input
            for char in inStr:
                bits.append(int(mult))
                if char == '1':
                    ans += mult
                elif char != '1' and char != '0':
                    # Change the contents of entry to not contain the invalid character
                    newStr = inStr.replace(char, "")
                    self.entry.set_text(newStr)

                    # Toast to tell the user binary only accepts 0 or 1 digits
                    wrongToast = Adw.Toast(
                        title="Binary only accepts the digits 0 and 1",
                        timeout=1.5,
                    )
                    self.overlay.add_toast(wrongToast)
                    return

                # Decrease the value of the bits until you arrive at 1 (or the end bit)
                mult = mult / 2

            # Remove brackets from the array string
            bitStr = str(bits).strip('[')
            bitStr = bitStr.strip(']')
            # Set the output label and bit counter label
            self.outLbl.set_text(f"{int(ans)}")
            self.bitLbl.set_text(f"Bits: {bitStr} ({len(inStr)} bits)")
        else:
            self.blank()

    def dec2bin(self, *kwargs):
        inStr = self.entry.get_text()

        if inStr != "":
            q = int(inStr) * 2
            r = 0
            result = ""
            ansBits = []
            bits = []

            while q > 0:
                r = q % 2
                q = q // 2
                ansBits.append(str(r))

            for x in range(len(ansBits) - 1, 0, -1):
                result = result + ansBits[x]

            for x in range(len(result), 0, -1):
                bits.append(int(pow(2, x) / 2))

            bitStr = str(bits).strip('[')
            bitStr = bitStr.strip(']')

            self.bitLbl.set_text(f"Bits: {bitStr} ({len(result)} bits)")
            self.outLbl.set_text(result)
        else:
            self.blank()

    def blank(self, *kwargs):
        # Return the label to it's original content
        self.outLbl.set_text("0")
        self.bitLbl.set_text("Bits: none")
