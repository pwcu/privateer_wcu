# Privateer: Wing Commander Universe (PWCU) - Developer Scripts

This directory contains developer utilities and automation scripts for building, packaging, and maintaining PWCU game assets.

---

## 1. Asset Data Conversion Pipeline (Vega Strike 0.9.x+)

Starting with Vega Strike engine 0.9.x (Asset API Version 2), game data formats transitioned from legacy CSV/XML files to JSON. The following developer scripts handle these conversions.

> [!NOTE]
> These scripts are **offline developer utilities**. The Vega Strike game engine does not run these scripts at runtime; it reads the generated `.json` files directly via native C++ loaders.

| Script | Source File | Output File | Description |
| :--- | :--- | :--- | :--- |
| [`script/convert_data.py`](convert_data.py) | *All below* | *All below* | **Master script**: Executes all data converters in sequence. |
| [`units/parser.py`](../units/parser.py) | `units/units.csv` | `units/units.json` | Parses all 473 unit definitions (ships, planets, bases, upgrades) into the monolithic units array expected by `UnitJSONFactory`. Auto-detects headers and provides guaranteed fallback to canonical schema. |
| [`script/convert_weapons.py`](convert_weapons.py) | `weapon_list.xml` | `weapons.json` | Converts XML weapon definitions into JSON objects consumed by the engine reload and weapon systems. |
| [`script/convert_parts.py`](convert_parts.py) | `master_part_list.csv` | `master_part_list.json` | Converts the trade cargo and upgrade parts manifest into JSON conforming to the `Cargo` constructor in `manifest.cpp`. Automatically sets `passenger` and `slave` flags. |

### Running the Data Conversion Pipeline

To regenerate all JSON data after editing CSV or XML source files:

```bash
./script/convert_data.py
```

Or run any converter individually:

```bash
# Convert units
python3 units/parser.py

# Convert weapons
./script/convert_weapons.py

# Convert cargo/parts
./script/convert_parts.py
```

---

## 2. Build & Packaging Scripts

| Script | Platform / Context | Description |
| :--- | :--- | :--- |
| [`script/build`](build) | Linux / POSIX | Configures CMake in the `build/` directory and checks build prerequisites. |
| [`script/build.ps1`](build.ps1) | Windows (PowerShell) | Configures CMake on Windows systems. |
| [`script/package`](package) | Linux / POSIX | Runs CPack to generate release packages (`.deb`, `.rpm`, `.tar.xz`) in the `packages/` directory. |
| [`script/package.ps1`](package.ps1) | Windows (PowerShell) | Runs CPack to generate release packages (`.zip`, NSIS installer) on Windows. |
| [`script/cibuild`](cibuild) | CI Automation | Cross-platform orchestration script invoked by GitHub Actions workflows for continuous integration and automated release packaging. |
| [`script/clean`](clean) | Linux / POSIX | Removes `build/` directory and compiled Python bytecode (`*.pyc`). |
| [`script/docker-entrypoint.sh`](docker-entrypoint.sh) | Docker / Container | Entrypoint script for reproducible containerized build environments. |

---

## 3. General Workflow for Data Updates

1. Modify source data in `units/units.csv`, `weapon_list.xml`, or `master_part_list.csv`.
2. Run `./script/convert_data.py` to regenerate the corresponding `.json` files.
3. Validate the build and packages locally:
   ```bash
   ./script/build
   ./script/package
   ./script/clean
   ```
4. Commit both the source files and the generated JSON files together.
