# Project guidance

This repository is the PF2E Remaster system and licensed content package for
Encounter+. Use `ROADMAP.md` for product decisions and `STATUS.md` for the
current handoff; read only the one relevant to the task.

- Treat `compendium/` as generated publication output. Repair the applicable
  source under `../structured-modules` or the deterministic builder/catalog in
  `tools/`, then rebuild the affected packs.
- Preserve GM editability: mechanics displayed by a form or view must remain
  available in the editor unless they are map-only load behavior.
- Prefer native Encounter+ entities, routes, rolls, and load actions. Keep
  panels usable at narrow in-app widths and preserve internal reference links.
- Keep ORC/OGL attribution and Reserved Material boundaries intact. Do not add
  undistributable prose merely because it exists in a local reference source.
- Extend the existing domain regression suite for a demonstrated failure; do
  not create a new test file for every fix.
- `python3 tools/eplus_dev.py check --json` is the single source-check command.
  It runs every maintained content and UI regression. Build a test package only
  when app verification is useful.
- Do not bump versions, push, or publish until requested. Commit completed local
  work and record pending native-app verification in `STATUS.md`.
