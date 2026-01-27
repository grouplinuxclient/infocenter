# SPDX-License-Identifier: GPL-2.0-or-later

import gi
import os
import requests
import socket

from .helper import _check_service, _check_local_proxy_port, _check_pac_file, set_test_value
from gettext import gettext as _

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Adw, Gtk  # noqa: E402

#DISPLAY_NAME = "Zsclaer Client Conector"

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
    plugin_group.set_title(_("Zscaler Client Connector"))
    plugin_group.set_description(
        _("System checks whether the Zscaler is properly set up and running")
    )

    running_label = _add_row(
        plugin_group,
        _("Application Running"),
        _("Check whether Zscaler is running"),
    )
    proxy_label = _add_row(
        plugin_group,
        _("Proxy"),
        _("Check whether the proxy port is accessible"),
    )
    pac_label = _add_row(
        plugin_group,
        _("PAC-File"),
        _("Check whether the PAC file is valid"),
    )

    set_test_value(running_label, _check_service("zsaservice"))
    set_test_value(proxy_label, _check_local_proxy_port(port = 9000, ip = "127.0.0.1"))
    set_test_value(pac_label, _check_pac_file(port = 9000, ip = "127.0.0.1"))
    return plugin_group
