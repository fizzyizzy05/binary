# main.py
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
        self.create_action('preferences', self.on_preferences_action)
        self.settings = Gio.Settings(schema_id="io.github.fizzyizzy05.binary")
        Adw.StyleManager.get_default().set_color_scheme(self.settings.get_int("preferred-theme"))

    def do_activate(self):
        """Called when the application is activated.

        We raise the application's main window, creating it if
        necessary.
        """
        win = self.props.active_window
        if not win:
            win = BinaryWindow(application=self)
        win.present()

    release_notes = """<p>
        Binary 0.2 is the latest update to the base converter app. This update introduces hexadecimal (or base 16) as a number base, allowing for conversions to and from hexadecimal numbers. The app also now has a green accent colour, making it feel more fun and distinctive. And invalid digits are now removed from the input box, making the app smoother and easier to use.
      </p>
      <p>
        Additionally, the following bug fixes and smaller improvements have been made:
      </p>
      <ul>
        <li>The output is now selectable, allowing for copy and paste instead of needing to manually type out the result.</li>
        <li>Decimal input now has data validation, and will display a toast when using an invalid digit.</li>
        <li>Wrong digit toasts will no longer duplicate, and will simply stay up when an invalid base is used.</li>
        <li>The bit counter has been updated to be cleaner and easier to understand.</li>
      </ul>"""

    def on_about_action(self, widget, _):
        """Callback for the app.about action."""
        about = Adw.AboutWindow(transient_for=self.props.active_window,
                                application_name='Binary',
                                application_icon='io.github.fizzyizzy05.binary',
                                developer_name='Izzy Jackson',
                                version='0.2',
                                developers=['Izzy Jackson'],
                                website="https://github.com/fizzyizzy05/binary/",
                                issue_url="https://github.com/fizzyizzy05/binary/issues/new",
                                license_type=Gtk.License.GPL_3_0,
                                release_notes_version='0.2.x',
                                release_notes=self.release_notes,
                                copyright='© 2023-2024 Izzy Jackson.')
        about.present()

    def on_preferences_action(self, widget, _):
        """Callback for the app.preferences action."""
        print('app.preferences action activated')
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


