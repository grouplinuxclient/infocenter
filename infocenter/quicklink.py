# SPDX-License-Identifier: GPL-2.0-or-later

import gi

gi.require_version("Gtk", "4.0")

from gi.repository import Gtk  # noqa E402


@Gtk.Template(resource_path="/de/volkswagen/infocenter/gtk/quicklink.ui")
class QuickLink(Gtk.Box):
    __gtype_name__ = "QuickLink"

    label = Gtk.Template.Child()
    button = Gtk.Template.Child()
    image = Gtk.Template.Child()

    def __init__(self, link, title, icon, **kwargs):
        super().__init__(**kwargs)
        self.label.set_label(title)
        self.button.set_uri(link)
        self.image.set_from_icon_name(icon)
