# SPDX-License-Identifier: GPL-2.0-or-later

from __future__ import annotations

import os
import socket
from typing import Iterable, Sequence


def _check_service(service: str) -> bool:
    """
    Checks with systemd if a service is running.
    Returns True if `systemctl is-active <service>` exits with 0.
    """
    try:
        ret = os.system(f"systemctl is-active {service} > /dev/null")
        return ret == 0
    except FileNotFoundError:
        return False
    except Exception:
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


def _check_interface(names: Sequence[str]) -> bool:
    try:
        interfaces = socket.if_nameindex()
        existing = [i[1] for i in interfaces]
        return any(name in existing for name in names)
    except ValueError:
        return False

def set_test_value(label, value):
        """
        Args:
            label (Adw.Label): Adwaita widget, whose text and CSS class is set
            value (bool): Test-Value, which will be interpreted as successful or failed
        """
        if value:
            label.set_label(_("Success"))
            label.add_css_class("success")
        else:
            label.set_label(_("Failed"))
            label.add_css_class("error")

