# Current status

Last updated: 2026-10-03

- Branch: `remaster-community-base`
- Package version: `1.701.9` (unchanged since the last published release)
- Latest completed local work: the Murajau, Lithic Locus, Solar Crow, Vault
  Builder, and Adult Executor Dragon audits now exercise source-driven creature
  generation rather than slug-specific patches. Printed or structured source
  data supplies Strike type and traits, numeric reach/range parameters,
  movement, ability placement, save details, weaknesses, items, and named Lore.
  Shared cleanup removes leaked empty rule elements and actor-only `unarmed`
  traits. Recall Knowledge derives every applicable subject and skill for all
  creatures, including multi-subject entries. Tests reject reintroducing a
  creature-specific override for the five audit examples and enforce the shared
  invariants across all generated packs.
- Automated baseline: the public ORC/OGL packs, package definitions, creature
  links and spellcasting, area templates, and maintained UI regressions pass
  through `python3 tools/eplus_dev.py check --json`.
- Native-app verification still required: import `dist/test/pf2e-remaster.system`
  and spot-check all five audit creatures. Confirm Murajau's ranged spear and
  active Retract, Lithic Locus's compact spell list, Solar Crow's printed Strike
  traits, Vault Builder's Speeds/range/save fields, and Adult Executor Dragon's
  save bonus, weakness, and numeric reach. Also confirm Recall subjects remain
  plain editable text while accepted skills remain internal links.
- Current product priority: continue the complete data audit and review upstream
  Encounter+ compatibility before releases. See `ROADMAP.md` for accepted,
  deferred, and completed feature decisions.

Update this file at a material handoff, app-test result, upstream merge, or
release. Do not use it as a chronological work log.
