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

# TODO: Update flatpak manifest in Flathub
import sys
import gi

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Gio, Adw
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
        self.settings = Gio.Settings(schema_id="io.github.fizzyizzy05.binary")

    def do_activate(self):
        """Called when the application is activated.

        We raise the application's main window, creating it if
        necessary.
        """
        win = self.props.active_window
        if not win:
            win = BinaryWindow(application=self)
        win.present()

    release_notes = """
        <p>Binary 0.3 is a new release with the following improvements:</p>
        <ul>
          <li>A new cleaner design for the base selectors for the headers.</li>
          <li>Added support for converting numbers between octal and other bases.</li>
          <li>Reworked number conversions to be more reliable and quicker.</li>
        </ul>
        <p>Added translations for the following locales:</p>
        <ul>
          <li>German (Konstantin Tutsch)</li>
          <li>Finnish (Jiri Grönroos)</li>
        </ul>
    """

    def on_about_action(self, *args):
        """Callback for the app.about action."""
        about = Adw.AboutWindow(transient_for=self.props.active_window,
                                application_name='Binary',
                                application_icon='io.github.fizzyizzy05.binary',
                                developer_name='Isabelle Jackson',
                                version='0.4',
                                developers=['Isabelle Jackson'],
                                issue_url="https://github.com/fizzyizzy05/binary/issues/",
                                license_type=Gtk.License.GPL_3_0,
                                release_notes_version='0.3.x',
                                release_notes=self.release_notes,
                                # Translators: Replace "translator-credits" with your names, one name per line
                                translator_credits = _("translator-credits"),
                                copyright='© 2023-2024 Isabelle Jackson.')
        about.present()

    def on_preferences_action(self, widget, _):
        """Callback for the app.preferences action."""
        prefsWindow = PrefsWindow()
        prefsWindow.set_transient_for(self.props.active_window)
        prefsWindow.present()

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


