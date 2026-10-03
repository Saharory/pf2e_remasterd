# Current status

Last updated: 2026-10-03

- Branch: `remaster-community-base`
- Package version: `1.701.9` (unchanged since the last published release)
- Latest completed local work: the creature audit remains fully source-driven,
  with no slug-specific patches for the five review examples. Recall Knowledge
  now stores editable subject-to-skill pairs, so multi-subject creatures render
  each classification with its own accepted skills. Creature immunities sort by
  their visible labels, action directives retain printed DCs, shared inline
  linking covers auditory and contextual move traits, and degree-of-success
  lines stay indented within their owning ability paragraph. The maintained
  creature regression enforces these rules across every generated pack.
- Automated baseline: the public ORC/OGL packs, package definitions, creature
  links and spellcasting, area templates, and maintained UI regressions pass
  through `python3 tools/eplus_dev.py check --json`.
- Native-app verification still required: import `dist/test/pf2e-remaster.system`
  and confirm Murajau's Retract links auditory and move, Solar Crow's Blinding
  Heat outcomes align like the dragon outcome block, and Lithic Locus renders
  three separately paired Recall Knowledge subjects, alphabetical immunities,
  and Escape DC 34 in Bury. Also open the creature editor and confirm each
  Recall Knowledge subject and its skills can be changed independently.
- Current product priority: continue the complete data audit and review upstream
  Encounter+ compatibility before releases. See `ROADMAP.md` for accepted,
  deferred, and completed feature decisions.

Update this file at a material handoff, app-test result, upstream merge, or
release. Do not use it as a chronological work log.
