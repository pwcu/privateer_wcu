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

# Canonical column headers defined for Vega Strike / PWCU units.
# Used for verification and as a guaranteed fallback if the CSV lacks a header row.
DEFAULT_HEADERS = [
    "Key", "Directory", "Name", "FoFID", "Object_Type",
    "Combat_Role", "Textual_Description", "Hud_image", "Unit_Scale", "Cockpit",
    "CockpitX", "CockpitY", "CockpitZ", "Mesh", "Shield_Mesh", "Rapid_Mesh", "BSP_Mesh",
    "Use_BSP", "Use_Rapid", "Mass", "Moment_Of_Inertia", "Convex_Hull_Volume",
    "Fuel_Capacity", "Hull", "Armor_Front_Top_Right", "Armor_Front_Top_Left",
    "Armor_Front_Bottom_Right", "Armor_Front_Bottom_Left", "Armor_Back_Top_Right",
    "Armor_Back_Top_Left", "Armor_Back_Bottom_Right", "Armor_Back_Bottom_Left", "Shield_Front_Top_Right",
    "Shield_Back_Top_Left", "Shield_Front_Bottom_Right", "Shield_Front_Bottom_Left",
    "Shield_Back_Top_Right", "Shield_Front_Top_Left", "Shield_Back_Bottom_Right",
    "Shield_Back_Bottom_Left", "Shield_Recharge", "Shield_Leak", "Warp_Capacitor",
    "Primary_Capacitor", "Reactor_Recharge", "Jump_Drive_Present", "Jump_Drive_Delay",
    "Wormhole", "Outsystem_Jump_Cost", "Warp_Usage_Cost", "Afterburner_Type",
    "Afterburner_Usage_Cost", "Maneuver_Yaw", "Maneuver_Pitch", "Maneuver_Roll",
    "Yaw_Governor", "Pitch_Governor", "Roll_Governor", "Afterburner_Accel",
    "Forward_Accel", "Retro_Accel", "Left_Accel", "Right_Accel", "Top_Accel",
    "Bottom_Accel", "Afterburner_Speed_Governor", "Default_Speed_Governor", "ITTS",
    "Radar_Color", "Can_Lock", "Radar_Range", "Tracking_Cone", "Max_Cone", "Lock_Cone", "Hold_Volume",
    "Can_Cloak", "Cloak_Min", "Cloak_Rate", "Cloak_Energy", "Cloak_Glass", "Repair_Droid",
    "ECM_Rating", "ECM_Resist", "Ecm_Drain", "Hud_Functionality", "Max_Hud_Functionality",
    "Lifesupport_Functionality", "Max_Lifesupport_Functionality", "Comm_Functionality",
    "Max_Comm_Functionality", "FireControl_Functionality", "Max_FireControl_Functionality",
    "SPECDrive_Functionality", "Max_SPECDrive_Functionality", "Slide_Start", "Slide_End",
    "Activation_Accel", "Activation_Speed", "Upgrades",
    "Sub_Units", "Sounds", "Light", "Mounts", "Net_Comm", "Dock", "Cargo_Import", "Cargo",
    "Explosion", "Equipment_Space", "Num_Animation_Stages", "Upgrade_Storage_Volume", "Heat_Sink_Rating",
    "Shield_Efficiency", "Num_Chunks", "Chunk_0", "Collide_Subunits", "Tractorability"
]

KNOWN_DATA_TYPES = {"key", "string", "float", "int", "bool", "boolean", "double"}


def is_header_row(row):
    """Detect if row contains column headers."""
    if not row:
        return False
    return row[0].strip().lower() == "key"


def is_type_row(row):
    """Detect if row contains column data type descriptors (e.g. String, float)."""
    if not row:
        return False
    non_empty = [cell.strip().lower() for cell in row[:10] if cell.strip()]
    if not non_empty:
        return False
    type_matches = sum(1 for cell in non_empty if cell in KNOWN_DATA_TYPES)
    return (type_matches / len(non_empty)) >= 0.5


def convert_units():
    if not os.path.exists(CSV_PATH):
        print(f"Error: {CSV_PATH} not found", file=sys.stderr)
        sys.exit(1)

    with open(CSV_PATH, mode="r", newline="", encoding="utf-8", errors="replace") as f:
        reader = csv.reader(f)
        try:
            first_row = next(reader)
        except StopIteration:
            print(f"Error: {CSV_PATH} is empty", file=sys.stderr)
            sys.exit(1)

        # Check if first row is a header row or data
        if is_header_row(first_row):
            headers = [h.strip() for h in first_row if h.strip()]
            # If the parsed header count doesn't match canonical headers, fallback to canonical
            if len(headers) != len(DEFAULT_HEADERS):
                print(f"Warning: Header count mismatch ({len(headers)} vs expected {len(DEFAULT_HEADERS)}). Falling back to canonical headers.")
                headers = DEFAULT_HEADERS
            data_rows = reader
        else:
            # First row is data, use canonical headers
            print("Notice: Header row not detected in CSV; applying canonical default headers.")
            headers = DEFAULT_HEADERS
            data_rows = [first_row] + list(reader)

        units = []
        for row in data_rows:
            if not row or is_type_row(row):
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
