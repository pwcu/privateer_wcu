#!/usr/bin/env python3
"""
Convert master_part_list.csv to master_part_list.json for Vega Strike engine.
Matches manifest.cpp (Cargo schema) and Assets-Production cargo formatting.
"""

import csv
import json
import os
import sys

REPO_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_PATH = os.path.join(REPO_DIR, "master_part_list.csv")
JSON_PATH = os.path.join(REPO_DIR, "master_part_list.json")

DEFAULT_KEYS = ("file", "categoryname", "price", "mass", "volume", "description")


def modify_item(item):
    cat = item.get("categoryname", "")
    f = item.get("file", "")
    if cat.startswith("Passengers"):
        item["passenger"] = True
    if f in ("Slaves", "Pilot"):
        item["passenger"] = True
        item["slave"] = True


def is_header_row(row):
    if not row:
        return False
    return row[0].strip().lower() == "file"


def convert_parts():
    if not os.path.exists(CSV_PATH):
        print(f"Error: {CSV_PATH} not found", file=sys.stderr)
        sys.exit(1)

    parts = []
    with open(CSV_PATH, mode="r", newline="", encoding="utf-8", errors="replace") as f:
        reader = csv.reader(f)
        try:
            first_row = next(reader)
        except StopIteration:
            print(f"Error: {CSV_PATH} is empty", file=sys.stderr)
            sys.exit(1)

        if is_header_row(first_row):
            data_rows = reader
        else:
            print("Notice: Header row not detected in master parts CSV; using canonical keys.")
            data_rows = [first_row] + list(reader)

        for row in data_rows:
            if not row or not row[0].strip():
                continue
            item = {}
            for k, v in zip(DEFAULT_KEYS, row):
                item[k] = v.strip()
            modify_item(item)
            parts.append(item)

    with open(JSON_PATH, "w", encoding="utf-8") as json_file:
        json.dump(parts, json_file, indent=4)

    print(f"Successfully converted {len(parts)} items from {CSV_PATH} to {JSON_PATH}")


if __name__ == "__main__":
    convert_parts()
