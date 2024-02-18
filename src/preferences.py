# prefs.py
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
from gi.repository import Gio
import math
from .window import BinaryWindow

@Gtk.Template(resource_path='/io/github/fizzyizzy05/binary/preferences.ui')
class PrefsWindow(Adw.PreferencesWindow):
    __gtype_name__ = 'PrefsWindow'
    themeSelect = Gtk.Template.Child()
    groupDigits = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.themeSelect.connect("notify", self.changeTheme)
        self.groupDigits.connect("notify", self.changeGroupDigits)
        self.settings = Gio.Settings(schema_id="io.github.fizzyizzy05.binary")

        # Change the selected theme so it isn't overridden when preferences is opened
        preferredTheme = self.settings.get_int("preferred-theme")
        if preferredTheme == 4:
            self.themeSelect.set_selected(2)
        else:
            self.themeSelect.set_selected(preferredTheme)

    def changeTheme(self, *kwargs):
        theme = self.themeSelect.get_selected()
        if theme == 0:
            Adw.StyleManager.get_default().set_color_scheme(0)
            self.settings.set_int("preferred-theme", 0)
        elif theme == 1:
            Adw.StyleManager.get_default().set_color_scheme(1)
            self.settings.set_int("preferred-theme", 1)
        elif theme == 2:
            Adw.StyleManager.get_default().set_color_scheme(4)
            self.settings.set_int("preferred-theme", 4)

    def changeGroupDigits(self, *kwargs):
        enabled = self.groupDigits.get_active()
        if enabled == True:
            self.settings.set_int("group-digits", 1)
        else:
            self.settings.set_int("group-digits", 0)

    def hello(self, *kwargs):
        print("hello")
