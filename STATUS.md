# Current status

Last updated: 2026-10-01

- Branch: `remaster-community-base`
- Package version: `1.701.9` (unchanged since the last published release)
- Latest completed local work: named Lore specialties remain plain stat values,
  while the Lore heading and all 17 general skills open imported, ORC-licensed
  Player Core records. Gameplay references no longer send users to web pages;
  known Adamantine, Crafting, and siege-weapon links resolve in-app, and the
  undescribed legacy Radiation trait remains honest plain text.
- Automated baseline: the public ORC/OGL packs, package definitions, creature
  links and spellcasting, area templates, and maintained UI regressions pass
  through `python3 tools/eplus_dev.py check --json`.
- Native-app verification still required: build/import the next test package
  and check a creature with a named Lore specialty, each linked skill page,
  Adamantine resistance exceptions, and the linked vehicle weapon-mount rules.
- Current product priority: continue the complete data audit and review upstream
  Encounter+ compatibility before releases. See `ROADMAP.md` for accepted,
  deferred, and completed feature decisions.

Update this file at a material handoff, app-test result, upstream merge, or
release. Do not use it as a chronological work log.
