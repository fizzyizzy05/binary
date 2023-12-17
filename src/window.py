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
import math

@Gtk.Template(resource_path='/io/github/fizzyizzy05/binary/window.ui')
class BinaryWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'BinaryWindow'

    outLbl = Gtk.Template.Child()
    overlay = Gtk.Template.Child()
    entry = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @Gtk.Template.Callback()
    def calc(self, *args):
        inStr = self.entry.get_text()

        if inStr != "":
            ans = 0
            mult = 1

            # Work out how long the binary
            for count in range(len(inStr) - 1):
                mult = mult * 2

            for char in inStr:
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

                mult = mult / 2

            self.outLbl.set_text(f"= {int(ans)}")
        else:
            # Return the label to it's original content
            self.outLbl.set_text("Output goes here")
