# SPDX-License-Identifier: GPL-2.0-or-later

import os
import socket

import gi
from gettext import gettext as _

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from .helper import _check_service, _check_interface, set_test_value
from gi.repository import Adw, Gtk  # noqa: E402

#DISPLAY_NAME = "Palo Alto GlobalProtect"



def _add_row(
    plugin_group: Adw.PreferencesGroup, title: str, subtitle: str
) -> Gtk.Label:
    row = Adw.ActionRow(title=title)
    row.set_subtitle(subtitle)

    status_label = Gtk.Label(label="…")
    status_label.set_xalign(1.0)

    row.add_suffix(status_label)
    row.set_activatable(False)

    plugin_group.add(row)
    return status_label

def add_to_preferences_page(
    set_test_value
):
    plugin_group = Adw.PreferencesGroup()
    plugin_group.set_title(_("Palo Alto GlobalProtect"))
    plugin_group.set_description(
        _("System checks whether GlobalProtect is properly set up and running")
    )

    service_label = _add_row(
        plugin_group,
        _("Service"),
        _("Check whether the GlobalProtect service is running"),
    )

    interface_label = _add_row(
        plugin_group,
        _("Interface"),
        _("Check whether the GlobalProtect network interface exists"),
    )

    set_test_value(service_label, _check_service("paloalto-vpn"))
    set_test_value(interface_label, _check_interface(("vpn", "tun")))
    return plugin_group
