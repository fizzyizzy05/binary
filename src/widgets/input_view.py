# window.py
#
# Copyright 2026 Isabelle Jackson
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
from gi.repository import Gio
from gettext import ngettext, dgettext

@Gtk.Template(resource_path='/io/github/fizzyizzy05/binary/widgets/input_view.ui')
class InputView(Adw.Bin):
    __gtype_name__ = 'BinaryInputView'

    base_selector = Gtk.Template.Child()
    bit_counter = Gtk.Template.Child()
    input_entry = Gtk.Template.Child()

    bases_dict = {
        2:_("Binary"),
        8:_("Octal"),
        10:_("Decimal"),
        16:_("Hexadecimal"),
        -1:_("Other")
    }

    bases = Gtk.StringList.new(None)

    for x in bases_dict:
        bases.append(bases_dict[x])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.base_selector.set_model(self.bases)

    @Gtk.Template.Callback()
    def change_bases(self, *kwargs):
        selected_base = list(self.bases_dict.keys())[self.base_selector.get_selected()]

        if selected_base == 2:
            self.bit_counter.set_visible(True)
        else:
            self.bit_counter.set_visible(False)

