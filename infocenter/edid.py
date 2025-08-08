# SPDX-License-Identifier: GPL-2.0-or-later

import glob
import struct
from collections import namedtuple
from gettext import gettext as _
from typing import Tuple

_STRUCT_FORMAT = (
    "<"  # little-endian
    "8s"  # constant header (8 bytes)
    "H"  # manufacturer id (2 bytes)
    "H"  # product id (2 bytes)
    "I"  # serial number (4 bytes)
    "B"  # manufactoring week (1 byte)
    "B"  # manufactoring year (1 byte)
    "B"  # edid version (1 byte)
    "B"  # edid revision (1 byte)
    "B"  # video input type (1 byte)
    "B"  # horizontal size in cm (1 byte)
    "B"  # vertical size in cm (1 byte)
    "B"  # display gamma (1 byte)
    "B"  # supported features (1 byte)
    "10s"  # color characteristics (10 bytes)
    "H"  # supported timings (2 bytes)
    "B"  # reserved timing (1 byte)
    "16s"  # EDID supported timings (16 bytes)
    "18s"  # description block 1 (18 bytes)
    "18s"  # description block 2 (18 bytes)
    "18s"  # descriptionblock 3 (18 bytes)
    "18s"  # description block 4 (18 bytes)
    "B"  # extension flag (1 byte)
    "B"
)  # checksum (1 byte)

_RawEdid = namedtuple(
    "_RawEdid",
    (
        "header",
        "manu_id",
        "prod_id",
        "serial_no",
        "manu_week",
        "manu_year",
        "edid_version",
        "edid_revision",
        "input_type",
        "width",
        "height",
        "gamma",
        "features",
        "color",
        "timings_supported",
        "timings_reserved",
        "timings_edid",
        "description_1",
        "description_2",
        "description_3",
        "description_4",
        "extension",
        "checksum",
    ),
)


def parse_edid(edid: bytes) -> Tuple[str, str]:
    model = ""
    serial = ""

    if struct.calcsize(_STRUCT_FORMAT) != 128:
        raise ValueError("Wrong edid size.")

    if sum(map(int, edid)) % 256 != 0:
        raise ValueError("Checksum mismatch.")

    unpacked = struct.unpack(_STRUCT_FORMAT, edid)
    raw_edid = _RawEdid(*unpacked)

    if raw_edid.header != b"\x00\xff\xff\xff\xff\xff\xff\x00":
        raise ValueError("Invalid header.")

    if raw_edid.description_2[3] == 0xFC:
        model = str(raw_edid.description_2[5:17].decode()).strip()
    elif raw_edid.description_3[3] == 0xFC:
        model = str(raw_edid.description_3[5:17].decode()).strip()
    elif raw_edid.description_4[3] == 0xFC:
        model = str(raw_edid.description_4[5:17].decode()).strip()

    if raw_edid.description_2[3] == 0xFF:
        serial = str(raw_edid.description_2[5:17].decode()).strip()
    elif raw_edid.description_3[3] == 0xFF:
        serial = str(raw_edid.description_3[5:17].decode()).strip()
    elif raw_edid.description_4[3] == 0xFF:
        serial = str(raw_edid.description_4[5:17].decode()).strip()

    return model, serial


def get_edid_sysfs():
    monitor_data = []

    for filename in glob.glob("/sys/class/drm/**/edid", recursive=False):
        with open(filename, "rb") as file:
            try:
                data = file.read(128)
                model, serial = parse_edid(data)
                if len(model) > 0:
                    monitor_model = model
                else:
                    monitor_model = _("Unknown")

                if len(serial) > 0:
                    monitor_serial = serial
                else:
                    monitor_serial = _("Unknown")

                monitor_data.append((monitor_model, monitor_serial))
            except struct.error:
                pass

    return monitor_data
