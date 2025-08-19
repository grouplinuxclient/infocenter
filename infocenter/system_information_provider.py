# SPDX-License-Identifier: GPL-2.0-or-later

import os
from infocenter.edid import get_edid


def get_os() -> str:
    info = {}

    with open("/etc/os-release") as os_release:
        for line in os_release:
            try:
                key, value = line.rstrip().split("=")

                info[key] = value.replace('"', "")
            except ValueError:
                pass

    if "PRETTY_NAME" in info:
        return info["PRETTY_NAME"]
    return "Unknown"


def get_hardware_model() -> str:
    hardware_model = "Unknown"
    with open("/sys/devices/virtual/dmi/id/product_name") as file:
        hardware_model = file.read().strip()
    return hardware_model


def get_bios_version() -> str:
    bios_version = "Unknown"
    with open("/sys/devices/virtual/dmi/id/bios_version") as file:
        bios_version = file.read().strip()
    return bios_version


def get_cpu_model() -> str:
    info = {}

    with open("/proc/cpuinfo") as proc_cpuinfo:
        data = proc_cpuinfo.read().split("\n")

        for line in data:
            try:
                key, value = line.rstrip().split(":")

                info[key.strip()] = value.replace('"', "").strip()
            except ValueError:
                pass

    if "model name" in info:
        return info["model name"]
    return "Unknown"


def get_kernel_version() -> str:
    kernel_version = "Unknown"
    with open("/proc/version") as file:
        kernel_version = file.read().strip()

    return kernel_version


def get_monitor_list() -> list:
    monitor_data = get_edid()
    return monitor_data


def get_language_short_code() -> str:
    lang = str(os.getenv("LANG"))

    if len(lang) > 2:
        return lang[:2]

    return "en"


def get_graphic_card_list() -> list:
    from pydbus import SystemBus

    graphics_data = []
    bus = SystemBus()
    switcheroo_config = bus.get(
        "net.hadess.SwitcherooControl", "/net/hadess/SwitcherooControl"
    )

    gpus = switcheroo_config.GPUs
    for gpu in gpus:
        graphics_data.append(gpu["Name"])

    return graphics_data
