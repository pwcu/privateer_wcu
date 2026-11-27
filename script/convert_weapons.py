#!/usr/bin/env python3
"""
Convert weapon_list.xml to weapons.json for Vega Strike engine.
Ported from Assets-Production convert.py.
"""

import json
import os
import sys
import xml.etree.ElementTree as et

REPO_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
XML_PATH = os.path.join(REPO_DIR, "weapon_list.xml")
JSON_PATH = os.path.join(REPO_DIR, "weapons.json")

STRING_KEYS = ["type", "name", "mountsize", "file", "soundwav"]


def convert_weapons():
    if not os.path.exists(XML_PATH):
        print(f"Error: {XML_PATH} not found", file=sys.stderr)
        sys.exit(1)

    weapon_xml = et.parse(XML_PATH)
    root = weapon_xml.getroot()

    weapons = []
    for elem in root:
        weapon_dict = {}
        weapon_dict["type"] = elem.tag
        weapon_dict.update(elem.attrib)

        for child in elem:
            prefix = child.tag
            for key, value in child.attrib.items():
                if key in STRING_KEYS:
                    weapon_dict[f"{prefix}.{key}"] = value
                else:
                    try:
                        weapon_dict[f"{prefix}.{key}"] = float(value)
                    except ValueError:
                        weapon_dict[f"{prefix}.{key}"] = value

        weapons.append(weapon_dict)

    with open(JSON_PATH, "w", encoding="utf-8") as json_file:
        json.dump(weapons, json_file, indent=4)

    print(f"Successfully converted {len(weapons)} weapons from {XML_PATH} to {JSON_PATH}")


if __name__ == "__main__":
    convert_weapons()
