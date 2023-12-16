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

@Gtk.Template(resource_path='/io/fizzyizzy05/binary/window.ui')
class BinaryWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'BinaryWindow'

    outLbl = Gtk.Template.Child()
    entry = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @Gtk.Template.Callback()
    def btnClick(self, *args):
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
                    # Pop up dialogue explaining that this number system only supports 1 and 0 as input
                    wrongChar = Adw.MessageDialog(
                        heading="Invalid input",
                        body="The binary number system only supports 1 and 0 as input",
                        close_response="okay",
                        modal=True,
                        transient_for=self
                    )
                    wrongChar.add_response("okay", "Okay")
                    wrongChar.choose(None)
                    return

                mult = mult / 2

            self.outLbl.set_text(f"= {int(ans)}")
        else:
            # Pop up dialogue explaining that this is a blank input
            blankIn = Adw.MessageDialog(
                heading="Blank input",
                body="The input you have given is blank",
                close_response="okay",
                modal=True,
                transient_for=self
            )
            blankIn.add_response("okay", "Okay")
            blankIn.choose(None)