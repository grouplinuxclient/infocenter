# SPDX-License-Identifier: GPL-2.0-or-later

import socket
import subprocess

import requests


def check_local_proxy_port(port: int = 9000, ip: str = "127.0.0.1") -> bool:
    """
    Checks if local proxy port is available.

    Args:
        port (int, optional): Defaults to 9000.
        ip (str, optional): Defaults to "127.0.0.1".

    Returns:
        bool: Returns the result of the proxy port check
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    return sock.connect_ex((ip, port)) == 0


def check_pac_file(port: int = 9000, ip: str = "127.0.0.1") -> bool:
    """
    Checks for proper pac file. This test will always fail if local proxy port check fails.

    Args:
        port (int, optional): Defaults to 9000.
        ip (str, optional): Defaults to "127.0.0.1".

    Returns:
        bool: Returns the test result
    """
    if check_local_proxy_port():
        try:
            response = requests.get(
                "http://{IP}:{PORT}/localproxy".format(IP=ip, PORT=port)
            ).content
            return True if response else False
        except Exception:
            return False
    return False


def check_zscaler_service(service: str = "zsaservice") -> bool:
    """
    Checks with systemd if Zscaler service is running. Does not check for Zscaler tunnel.

    Args:
        service (str, optional): Defaults to "zsaservice"

    Returns:
        bool: Returns true if Zsacler service is running
    """
    try:
        process = subprocess.Popen(
            ["systemctl", "is-active", service], stdout=subprocess.PIPE
        )
        (result, err) = process.communicate()
        return result.decode("utf-8").strip().__eq__("active")
    except FileNotFoundError:
        return False


def check_vpn() -> bool:
    """
    Checks the presence of virtual network interfaces by their names (gpd0, vpn0, tun0)

    Returns:
        bool: Returns true if virtual network interfaces are present
    """
    try:
        interfaces = socket.if_nameindex()
        names = [i[1] for i in interfaces]
        return any(i in names for i in ("gpd0", "vpn0", "tun0"))
    except ValueError:
        return False
