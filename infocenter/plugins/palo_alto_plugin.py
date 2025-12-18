# SPDX-License-Identifier: GPL-2.0-or-later

import os
import socket

import gi
from gettext import gettext as _

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Adw, Gtk  # noqa: E402

DISPLAY_NAME = "Palo Alto GlobalProtect"


def _check_paloalto_service(service: str = "paloalto-vpn") -> bool:
    try:
        ret = os.system(f"systemctl is-active {service} > /dev/null")
        return ret == 0
    except FileNotFoundError:
        return False


def _check_paloalto_interface(names=("pa0", "vpn-pa0", "tun_pa0")) -> bool:
    try:
        interfaces = socket.if_nameindex()
        existing = [i[1] for i in interfaces]
        return any(name in existing for name in names)
    except ValueError:
        return False


def check() -> bool:
    return _check_paloalto_service() and _check_paloalto_interface()


def run_check() -> bool:
    return check()


def add_to_preferences_page(
    preference_page, set_test_value, plugin_type=None, display_name=None
):
    title = display_name or DISPLAY_NAME
    if plugin_type:
        title = f"{title} ({plugin_type})"

    plugin_group = Adw.PreferencesGroup()
    plugin_group.set_title(title)

    row = Adw.ActionRow(title=_("Status"))
    status_label = Gtk.Label(label="…")
    status_label.set_xalign(1.0)
    row.add_suffix(status_label)
    row.set_activatable(False)

    plugin_group.add(row)
    preference_page.add(plugin_group)

    set_test_value(status_label, run_check())
