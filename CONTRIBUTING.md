# Contributing to Privateer: Wing Commander Universe

Welcome to **Privateer: Wing Commander Universe** (PWCU)!

There are many ways to contribute: 3D models and textures, missions and campaigns, Python scripting, audio and voice acting, balancing, documentation, and bug testing.

## Community & Communications

Development discussions and community coordination happen in:

* **PWCU Matrix Room:** [#vegastrike_pwcu:gitter.im](https://matrix.to/#/#vegastrike_pwcu:gitter.im)
* **Vega Strike Community Room:** [#vegastrike_community:gitter.im](https://matrix.to/#/#vegastrike_community:gitter.im)
* **Forums:** [Vega Strike Forums](https://forums.vega-strike.org/)

## Relationship with the Vega Strike Engine

PWCU contains game assets, campaigns, and Python runtime logic. The underlying engine lives in [vegastrike/Vega-Strike-Engine-Source](https://github.com/vegastrike/Vega-Strike-Engine-Source). If your change requires engine-level modifications, coordinate with the engine team and prepare two pull requests (one for each repository).

## Contribution Guidelines

1. **Python 3 Compatibility:** All scripts in `bases/`, `modules/`, and `tools/` run under Python 3 embedded in the engine. All files must compile cleanly with `python3 -W error -m py_compile`.
2. **Asset Conversion Pipeline:** For Vega Strike 0.9.x+, game data is stored in JSON manifests (`units/units.json`, `weapons.json`, `master_part_list.json`). When editing source CSV or XML files, always run `./script/convert_data.py` and commit both the source and generated files together.
3. **Playtesting:** Before submitting a pull request that alters missions, cockpits, bases, or unit definitions, verify that the game boots cleanly with `vegastrike-engine -D .` without exceptions or crashes.
4. **Git Workflow:**
   - Create focused feature branches off `master` (e.g. `feat/...`, `fix/...`, `chore/...`).
   - Use conventional commit messages.
   - Follow the `.github/pull_request_template.md` checklist when opening a PR.
5. **Coding Standards & Formatting:** Follow `.editorconfig` (UTF-8, LF line endings, 2 spaces for JSON/YAML/shell, 4 spaces for Python/CMake).
6. **AI Contributions:** If you use AI coding assistants, refer to [AGENTS.md](AGENTS.md). AI contributions should be credited using the git commit trailer `Co-authored-by: <Agent> <email>` and never added to copyright ownership lines.
