# SPDX-License-Identifier: GPL-2.0-or-later

import os
import socket
import gi
import requests
from gettext import gettext as _

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Adw, Gtk  # noqa: E402


def _check_zscaler_service(service: str = "zsaservice") -> bool:
    """
    Checks with systemd if Zscaler service is running
    """
    try:
        ret = os.system(f"systemctl is-active {service} > /dev/null")
        return ret == 0
    except FileNotFoundError:
        return False


def _check_local_proxy_port(port: int = 9000, ip: str = "127.0.0.1") -> bool:
    """Checks if the local Zscaler proxy port is reachable."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        return sock.connect_ex((ip, port)) == 0
    finally:
        try:
            sock.close()
        except Exception:
            pass


def _check_pac_file(port: int = 9000, ip: str = "127.0.0.1") -> bool:
    """Checks for a valid PAC file endpoint.

    This test will always fail if the local proxy port check fails.
    """
    if not _check_local_proxy_port(port=port, ip=ip):
        return False

    try:
        response = requests.get(f"http://{ip}:{port}/localproxy", timeout=2).content
        return bool(response)
    except Exception:
        return False


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
    preference_page, set_test_value, plugin_type=None, display_name=None
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

    preference_page.add(plugin_group)

    set_test_value(running_label, _check_zscaler_service())
    set_test_value(proxy_label, _check_local_proxy_port())
    set_test_value(pac_label, _check_pac_file())
