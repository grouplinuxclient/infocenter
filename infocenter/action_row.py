# SPDX-License-Identifier: GPL-2.0-or-later

import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")

from gi.repository import Adw, Gtk  # noqa E402


@Gtk.Template(resource_path="/de/volkswagen/infocenter/gtk/action-row.ui")
class ActionRow(Adw.ActionRow):
    __gtype_name__ = "ActionRow"

    def __init__(self, key=None, value="", **kwargs):
        super().__init__(title=key, **kwargs)
        self.set_subtitle(value)
