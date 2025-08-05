# SPDX-License-Identifier: GPL-2.0-or-later

from gettext import gettext as _
from pathlib import Path
import infocenter.system_check as system_check
import sys
import gi


gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")

from gi.repository import Adw, Gio, Gtk, GLib  # noqa E402

from infocenter.window import Window  # noqa E402


class Application(Adw.Application):
    """The main application singleton class."""

    def __init__(self):
        super().__init__(
            application_id="de.volkswagen.infocenter",
            flags=Gio.ApplicationFlags.HANDLES_COMMAND_LINE,
        )
        self.autostart = False
        self.create_action("quit", lambda *_: self.quit(), ["<primary>q"])
        self.create_action("about", self.on_about_action)
        self.create_action("journal", self.on_journal_action)
        self.add_main_option(
            "autostart",
            ord("a"),
            GLib.OptionFlags.NONE,
            GLib.OptionArg.NONE,
            "Autostart",
            None,
        )

    def do_activate(self):
        """Called when the application is activated.

        We raise the application's main window, creating it if
        necessary.
        """
        info_center_dir = Path.joinpath(Path.home(), ".config/infocenter")
        info_center_dir.mkdir(parents=True, exist_ok=True)

        if self.autostart:
            do_not_start_file = Path.joinpath(
                Path.home(), ".config/infocenter/do_not_start_file"
            )

            if Path(do_not_start_file).exists():
                print("do_not_start file present, exit.")
                return

        win = self.props.active_window
        if not win:
            win = Window(application=self)

        win.present()

    def on_journal_action(self, widget, _unused):
        """
        Action for journal export in menu button
        """
        dialog = Gtk.FileDialog(
            accept_label="Export",
            title=_("Export Journal to File"),
            initial_name="journal.txt",
            modal=True,
        )

        def response(dialog, result):
            if result.had_error():
                return
            filepath = Path(dialog.save_finish(result).get_path())
            system_check.write_journal(filepath)

        dialog.save(parent=self.props.active_window, callback=response)

    def on_about_action(self, widget, _):
        """Invoked when we click "about" in the main menu."""
        builder = Gtk.Builder.new_from_resource(
            "/de/volkswagen/infocenter/about_dialog.ui",
        )
        about_dialog = builder.get_object("about_dialog")
        about_dialog.present(self.props.active_window)

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

    def do_command_line(self, command_line):
        options = command_line.get_options_dict()
        if options.contains("autostart"):
            self.autostart = True

        self.activate()
        return 0


def main(version):
    """The application's entry point."""
    app = Application()
    return app.run(sys.argv)
