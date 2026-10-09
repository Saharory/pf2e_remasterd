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
  It runs every maintained content and UI regression.
- After each completed system implementation or fix, always build an installable
  game system for user testing with `tools/package_public_release.py`. Keep the
  latest package at `dist/test/pf2e-remaster.system`; remove older `.system`
  packages from the test folder only after the replacement passes archive
  inspection and its packaged definitions match the current source. Refresh
  the companion checksums/metadata and link the package in the handoff. This
  standing user instruction applies even while native testing is paused; a
  package build does not prove app behavior or authorize a release/version bump.
- Do not bump versions, push, or publish until requested. Commit completed local
  work and record pending native-app verification in `STATUS.md`.

- Versioning: one version bump per authorized push, as specified by the user.
  Do not increment repeatedly during testing or release preparation; use the
  user-approved version for the push. The 2026-10-10 release is 0.9.02.
