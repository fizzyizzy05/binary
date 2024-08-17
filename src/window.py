# window.py
#
# Copyright 2023-2024 Isabelle Jackson
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
import math

# Scripts used to calculate numbers
from .bit_count import *
from .get_answer import *

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
    in_spin = Gtk.Template.Child()
    out_spin = Gtk.Template.Child()

    # Translators: this string is used to describe how many bits there are.
    bits_text = _("bits")

    bases = Gtk.StringList.new(None)
    bases.append(_("Binary"))
    bases.append(_("Octal"))
    bases.append(_("Decimal"))
    bases.append(_("Hexadecimal"))
    bases.append(_("Other"))

    bases_dict = {
        0:2,
        1:8,
        2:10,
        3:16,
        4:-1
    }

    editable = False

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.in_dropdown.set_model(self.bases)
        self.out_dropdown.set_model(self.bases)

        close_action = Gio.SimpleAction(
            name="close",
        )
        close_action.connect(
            "activate",
            self.close_window,
        )

        self.in_spin.set_range(2, 36)
        self.in_spin.set_snap_to_ticks(True)
        self.in_spin.set_increments(1,2)
        self.out_spin.set_range(2, 36)
        self.out_spin.set_snap_to_ticks(True)
        self.out_spin.set_increments(1,2)

        self.settings = Gio.Settings(schema_id="io.github.fizzyizzy05.binary")
        self.settings.bind("input-base", self.in_dropdown, "selected",
                           Gio.SettingsBindFlags.DEFAULT)
        self.settings.bind("output-base", self.out_dropdown, "selected",
                           Gio.SettingsBindFlags.DEFAULT)
        self.input_entry.grab_focus()
        self.blank()

    @Gtk.Template.Callback()
    def change_input_base(self, *kwargs):
        try:
            self.output_handler()
            self.toggle_bit_counter()
            self.toggle_base_spin()
            self.editable = True
        except:
            return

    @Gtk.Template.Callback()
    def change_output_base(self, *kwargs):
        try:
            self.input_handler()
            self.toggle_bit_counter()
            self.toggle_base_spin()
            self.editable = True
        except:
            return

    @Gtk.Template.Callback()
    def input_handler(self, *kwargs):
        self.editable = False
        in_str = self.input_entry.get_text()
        ans = ""
        if in_str != "":
            if self.out_dropdown.get_selected() < 4:
                out_base = self.bases_dict[self.out_dropdown.get_selected()]
            else:
                out_base = int(self.out_spin.get_value())
            if self.in_dropdown.get_selected() < 4:
                in_base = self.bases_dict[self.in_dropdown.get_selected()]
            else:
                in_base = int(self.in_spin.get_value())
            ans = get_answer(in_str, in_base, out_base)
            if ans == "char":
                self.input_entry.add_css_class("error")
                self.input_entry.set_tooltip_text(_("Invalid input"))
                self.output_entry.set_tooltip_text(None)
            elif ans == "char_dual":
                self.input_entry.add_css_class("error")
                self.input_entry.set_tooltip_text(_("Invalid input"))
                self.output_entry.add_css_class("error")
                self.output_entry.set_tooltip_text(_("Invalid input"))
                self.output_entry.set_text(in_str)
            else:
                self.output_entry.set_text(ans)
                self.input_entry.remove_css_class("error")
                self.output_entry.remove_css_class("error")
                self.output_entry.set_tooltip_text(None)
                for char in in_str:
                    if char.islower():
                        self.input_entry.set_text(in_str.upper())
                        self.input_entry.set_position(-1)
                        return
        else:
            self.blank()
        self.toggle_mono()
        if ans != "char" and ans != "char_dual":
            self.update_bits()
        self.editable = True

    @Gtk.Template.Callback()
    def output_handler(self, *kwargs):
        if self.editable == True:
            in_str = self.output_entry.get_text()
            ans = ""
            if in_str != "":
                if self.out_dropdown.get_selected() < 4:
                    in_base = self.bases_dict[self.out_dropdown.get_selected()]
                else:
                    in_base = int(self.out_spin.get_value())
                if self.in_dropdown.get_selected() < 4:
                    out_base = self.bases_dict[self.in_dropdown.get_selected()]
                else:
                    out_base = int(self.in_spin.get_value())
                ans = get_answer(input=in_str, in_base=in_base, out_base=out_base)
                if ans == "char":
                    self.output_entry.add_css_class("error")
                    self.input_entry.remove_css_class("error")
                    self.output_entry.set_tooltip_text(_("Invalid input"))
                    self.input_entry.set_tooltip_text(None)
                elif ans == "char_dual":
                    self.input_entry.add_css_class("error")
                    self.input_entry.set_tooltip_text(_("Invalid input"))
                    self.output_entry.add_css_class("error")
                    self.output_entry.set_tooltip_text(_("Invalid input"))
                    self.input_entry.set_text(in_str)
                else:
                    self.input_entry.set_text(ans)
                    self.input_entry.remove_css_class("error")
                    self.output_entry.remove_css_class("error")
                    self.input_entry.set_tooltip_text(None)
                self.output_entry.set_position(-1)
            else:
                self.blank()
            self.toggle_mono()
            if ans != "char" and ans != "char_dual":
                self.update_bits()
            self.editable = True

    def blank(self, *kwargs):
        # Return the label to it's original content. Using a function for this ensures it's always the same value, and makes it more consistent.
        self.output_entry.set_text("")
        self.input_entry.set_text("")
        self.in_bit_label.set_label(f"0 {self.bits_text}")
        self.out_bit_label.set_label(f"0 {self.bits_text}")
        self.update_bits()
        self.toggle_mono()
        self.input_entry.remove_css_class("error")
        self.output_entry.remove_css_class("error")

    def update_bits(self, *kwargs):
        in_count = len(self.input_entry.get_text())
        out_count = len(self.output_entry.get_text())
        if in_count > 0 and out_count > 0:
            self.in_bit_label.set_label(f"{in_count} {self.bits_text}")
            self.input_bits.set_label(f"{bit_count(self.input_entry.get_text())}")
            self.out_bit_label.set_label(f"{out_count} {self.bits_text}")
            self.output_bits.set_label(f"{bit_count(self.output_entry.get_text())}")
        else:
            bit_counter_text = _("Enter a number to see its bits")
            self.input_bits.set_text(bit_counter_text)
            self.output_bits.set_text(bit_counter_text)

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

    def toggle_base_spin(self, *kwargs):
        if self.in_dropdown.get_selected() == 4:
            self.in_spin.set_visible(True)
        else:
            self.in_spin.set_visible(False)
        if self.out_dropdown.get_selected() == 4:
            self.out_spin.set_visible(True)
        else:
            self.out_spin.set_visible(False)

    def close_window(self, *kwargs):
        self.close()
