# AGENTS.md

Working notes for AI coding agents (Claude Code, Cursor, Codex, Copilot, pi, Gemini, and friends) operating
in this repository: what it is, how it builds, how the assets and scripts are laid out, and which
conventions changes are reviewed against.

**`README.md` and repository docs are authoritative.** Where this file disagrees with project standards,
this file should be corrected.

## What this repository is

The **game assets, Python runtime, and campaign data** for **Privateer: Wing Commander Universe** (`pwcu`).
It contains star systems, missions, ships, cockpits, base interfaces, audio, and trade manifests designed
to run against the Vega Strike core engine (Asset API Version 2 / Engine 0.9.x series).

Engine source code lives in the separate
[`vegastrike/Vega-Strike-Engine-Source`](https://github.com/vegastrike/Vega-Strike-Engine-Source)
repository. A change that spans both needs two pull requests, one per repository.

Branches:

- `master` — development head for PWCU targeting current Vega Strike engine releases (0.9.x).
- `0.8.x`, `0.7.x`, `0.6.x`, `0.5.x` — maintenance release lines matching historical engine releases.
  Do not target older maintenance branches unless explicitly asked to backport a fix.
- Follow conventional feature branch naming for active pull requests (e.g. `feat/*`, `fix/*`, `chore/*`).

## Build, package, and test

Asset packaging uses CMake 3.21+ and the helper scripts in `script/`:

```bash
# Configure and check build environment:
./script/build

# Generate release packages (deb, rpm, source tarball in packages/):
./script/package

# Clean build artifacts:
./script/clean
```

### Running with the engine

Running PWCU requires the compiled `vegastrike-engine` binary. Specify the repository directory
via `-D`:

```bash
# Launch into main game / base:
vegastrike-engine -D /path/to/privateer_wcu

# Direct mission launch:
vegastrike-engine -D /path/to/privateer_wcu mission/priv.mission
```

**A manual playtest is mandatory.** Before opening a PR that alters missions, base scripts, cockpits,
or asset definitions, launch the game with `vegastrike-engine` and verify that the game boots cleanly,
transitions between base and flight, and functions without console exceptions or crashes.

## Asset layout

| Path | Contents |
|---|---|
| `bases/` | Base concourses, bars, ship dealers, upgrade terminals, and fixer rooms (`bases/*.py`) |
| `cockpits/` | 2D cockpit overlays, MFD displays, and instrumentation for Privateer craft (`.cpt`) |
| `mission/` | Mission definitions and campaign milestones (`.mission`) |
| `modules/` | Python game logic: `GUI.py`, AI routines, quest managers, dynamic news, campaign state |
| `sectors/` | Star system XML definitions (`.system`): Gemini Sector, frontier, and Kilrathi systems |
| `sounds/` | Audio effects, bartender speech, campaign voiceovers, and weapon sounds (`.wav`) |
| `sprites/` | 2D sprite descriptors (`.spr`) and interface graphics |
| `techniques/`, `programs/` | Rendering technique trees and shader configurations |
| `textures/` | Skyboxes, planets, backgrounds, and ship materials |
| `units/` | Ship unit definitions (`units.json`, `units.csv`), textures, and 3D meshes (`.bfxm`) |
| `universe/` | Wing Commander sector connection graph (`universe/milky_way.xml`) |
| Root manifests & data | Economy and weapon manifests: `master_part_list.json`, `weapons.json`, `factions.xml` |
| `script/` | Build, CI, packaging, and data conversion tooling |

## Asset Data Conversion Pipeline

Starting with Vega Strike 0.9.x (Asset API Version 2), game data uses JSON instead of legacy CSV/XML.
Whenever you modify the source data files, run the conversion scripts to regenerate the corresponding JSON:

```bash
# Regenerate all JSON manifests in one command:
./script/convert_data.py
```

- `units/parser.py`: Converts `units/units.csv` &rarr; `units/units.json` (473 units, 117-column schema).
- `script/convert_weapons.py`: Converts `weapon_list.xml` &rarr; `weapons.json`.
- `script/convert_parts.py`: Converts `master_part_list.csv` &rarr; `master_part_list.json`.

Always commit both the source file (`.csv`/`.xml`) and the generated `.json` file together.

## Facts worth knowing before you dig

- **Asset API Version 2 requires JSON manifests.** Engine 0.9.0 reads `units/units.json`, `weapons.json`,
  and `master_part_list.json` via native C++ loaders. Do not delete the source CSV/XML files as they
  remain the editable canonical sources.
- **Python 3 compatibility is mandatory.** All scripts in `bases/`, `modules/`, and `tools/` run
  under Python 3 embedded in the engine. All files must compile cleanly with `python3 -W error -m py_compile`.
- **In Engine 0.9.x, graphical settings use `vegastrike.config`.** The in-game settings overlay (`Alt+C`)
  and `config.json` belong to engine 0.10.x+; 0.9.x still utilizes `vegastrike.config` and `vegasettings`.
- **Trailing empty unit entries cause engine crashes.** `units/units.json` must strictly contain valid,
  keyed unit objects. `units/parser.py` automatically strips empty rows to prevent startup crashes.
- **Authentic Wing Commander Lore.** Maintain authentic Privateer ship names (*Tarsus*, *Centurion*,
  *Orion*, *Galaxy*, *Stiletto*, *Gladius*, *Demon*, *Dralthi*, *Krant*), commodities (*Brilliance*, *Slaves*,
  *Ultimate*), and factions (*Confed*, *Militia*, *Merchant*, *Hunter*, *Pirates*, *Retro*, *Kilrathi*).

## Conventions and style

1. **Do not introduce unnecessary diff churn.** When editing manifests, configs, or scripts, touch
   only the relevant keys or blocks. Do not reformat entire unaffected files.
2. **Follow `.editorconfig`.** UTF-8 encoding, LF line endings, 2 spaces for JSON/YAML/shell,
   4 spaces for Python and CMake, no trailing whitespace.
3. **No local or private paths in committed files.** Never hard-code `/home/...` or user-specific
   directories in missions, configs, or scripts.
4. **One logical change per commit.** Provide a clear conventional commit message (`feat: ...`,
   `fix: ...`, `chore: ...`) explaining what was changed and why.
5. **Licensing is GPLv3-or-later.** Keep file copyright headers intact. AI agents are credited via
   the git commit trailer `Co-authored-by: Antigravity <antigravity@google.com>` and are never added
   to copyright holder lines.
6. **Pull Requests.** Every PR should fill out the checklist in `.github/pull_request_template.md`
   indicating tests run and the purpose of the change.

## When in doubt

Consult existing reference implementations in [`vegastrike/Assets-Production`](https://github.com/vegastrike/Assets-Production)
or [`vegastrike/vsu-black-paralysis`](https://github.com/vegastrike/vsu-black-paralysis), ask on the pull request,
or chat with the developers on [Matrix / Gitter (`#vegastrike_pwcu:gitter.im`)](https://matrix.to/#/#vegastrike_pwcu:gitter.im).
