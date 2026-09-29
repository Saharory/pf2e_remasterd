# Current status

Last updated: 2026-09-29

- Branch: `remaster-community-base`
- Package version: `1.701.9` (unchanged since the last published release)
- Latest completed local work: creature spellcasting, shared ability links, and
  structured creature metadata restoration through commit `55d5795`.
- Automated baseline: the public ORC/OGL packs, package definitions, creature
  links and spellcasting, area templates, and maintained UI regressions pass
  through `python3 tools/eplus_dev.py check --json`.
- Native-app verification still required: the creature metadata test package
  from `55d5795`, especially imprecise senses, trait-derived immunities,
  Hardness, telepathy/language details, and editable fields.
- Current product priority: continue the complete data audit and review upstream
  Encounter+ compatibility before releases. See `ROADMAP.md` for accepted,
  deferred, and completed feature decisions.

Update this file at a material handoff, app-test result, upstream merge, or
release. Do not use it as a chronological work log.
