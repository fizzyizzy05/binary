# main.py
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

import sys
import gi

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Gio, Adw, GLib
from .window import BinaryWindow
from .preferences import PrefsWindow

class BinaryApplication(Adw.Application):
    """The main application singleton class."""

    def __init__(self):
        super().__init__(application_id='io.github.fizzyizzy05.binary',
                         flags=Gio.ApplicationFlags.DEFAULT_FLAGS)
        self.create_action('quit', lambda *_: self.quit(), ['<primary>q'])
        self.create_action('about', self.on_about_action)
        self.create_action('preferences', self.on_preferences_action, None)
        self.create_action('close-window', self.on_close_window_action, ['<primary>w'])
        self.create_action('new-window', self.on_new_window_action, ['<primary>n'])
        self.settings = Gio.Settings(schema_id="io.github.fizzyizzy05.binary")
        Gtk.Window.set_default_icon_name('io.github.fizzyizzy05.binary')

        self.add_main_option("new-window", b"w", GLib.OptionFlags.NONE,
                             GLib.OptionArg.NONE, "Open a new window", None)

    def do_activate(self):
        """Called when the application is activated.

        We raise the application's main window, creating it if
        necessary.
        """
        if self.props.active_window:
            self.props.active_window.present()
        else:
            self.new_window()

    def do_handle_local_options(self, options):
        if options.contains("new-window"):
            self.register()
            if self.get_property("is-remote"):
                self.activate_action("new-window")
                return 0

        return -1

    def new_window(self):
        win = BinaryWindow(application=self)
        win.present()

    def on_new_window_action(self, *args):
        self.new_window()

    def on_about_action(self, *args):
        """Callback for the app.about action."""
        about = Adw.AboutDialog.new_from_appdata("io/github/fizzyizzy05/binary/metainfo.xml", "5.2")
        about.set_developers(["Isabelle Jackson https://fizzyizzy05.codeberg.page"])
        about.set_designers(["Gregor Niehl https://gitlab.gnome.org/gregorni"])
        # Translators: Replace "translator-credits" with your names, one name per line
        about.set_translator_credits(_("translator-credits"))
        about.set_copyright("© 2023-2024 Isabelle Jackson.")
        about.present(self.props.active_window)

    def on_preferences_action(self, widget, _):
        """Callback for the app.preferences action."""
        prefsWindow = PrefsWindow()
        prefsWindow.set_transient_for(self.props.active_window)
        prefsWindow.present()

    def on_close_window_action(self, *args):
        self.props.active_window.close()

    def create_action(self, name, callback, shortcuts=None):
        """Add an application action.

        Args:
            name: the name of the action
            callback: the function to be called when the action is
              activated
            shortcuts: an optional list of accelerators
        """
        action = Gio.SimpleAction.new(name, None)
        action.connect("activate", callback)
        self.add_action(action)
        if shortcuts:
            self.set_accels_for_action(f"app.{name}", shortcuts)


def main(version):
    """The application's entry point."""
    app = BinaryApplication()
    return app.run(sys.argv)


