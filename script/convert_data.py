#!/usr/bin/env python3
"""
Orchestration script to convert all asset data to JSON formats for Vega Strike 0.9.x:
  - units/units.csv -> units/units.json
  - weapon_list.xml -> weapons.json
  - master_part_list.csv -> master_part_list.json
"""

import os
import subprocess
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_DIR = os.path.dirname(SCRIPT_DIR)


def main():
    converters = [
        ("Units", [sys.executable, os.path.join(REPO_DIR, "units", "parser.py")]),
        ("Weapons", [sys.executable, os.path.join(SCRIPT_DIR, "convert_weapons.py")]),
        ("Parts", [sys.executable, os.path.join(SCRIPT_DIR, "convert_parts.py")]),
    ]

    for name, cmd in converters:
        print(f"--- Converting {name} ---")
        ret = subprocess.run(cmd, cwd=REPO_DIR)
        if ret.returncode != 0:
            print(f"Error: Failed to convert {name}", file=sys.stderr)
            sys.exit(ret.returncode)

    print("--- All asset data converted successfully! ---")


if __name__ == "__main__":
    main()
