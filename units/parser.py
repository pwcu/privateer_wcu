#!/usr/bin/env python3
"""
Convert units.csv to units.json for Vega Strike engine.
"""

import csv
import json
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(SCRIPT_DIR, "units.csv")
JSON_PATH = os.path.join(SCRIPT_DIR, "units.json")


def convert_units():
    if not os.path.exists(CSV_PATH):
        print(f"Error: {CSV_PATH} not found", file=sys.stderr)
        sys.exit(1)

    with open(CSV_PATH, mode="r", newline="", encoding="utf-8", errors="replace") as f:
        reader = csv.reader(f)
        headers = next(reader)
        # Row 1 contains column data types (e.g. Key, String, float, string...)
        _ = next(reader)

        units = []
        for line_num, row in enumerate(reader, start=3):
            if not row:
                continue
            # Skip rows without a Key or with empty key (prevents engine crashes)
            key = row[0].strip() if len(row) > 0 else ""
            if not key:
                continue

            unit = {}
            for header, val in zip(headers, row):
                val_clean = val.strip()
                if val_clean:
                    unit[header] = val_clean
            units.append(unit)

    with open(JSON_PATH, mode="w", encoding="utf-8") as f:
        json.dump(units, f, indent=4)

    print(f"Successfully converted {len(units)} units from {CSV_PATH} to {JSON_PATH}")


if __name__ == "__main__":
    convert_units()
