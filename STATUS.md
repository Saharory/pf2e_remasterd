# Current status

Last updated: 2026-10-03

- Branch: `remaster-community-base`
- Package version: `1.701.9` (unchanged since the last published release)
- Latest completed local work: the creature editor now exposes lossless,
  structured controls for special senses, searchable inventory items and
  quantities, immunity references/custom text, and ritual lists. Named Lore is
  edited inside the same Skills page, Recall Knowledge binds its complete
  knowledge-to-skill pairs, language and special-save notes have clear labels,
  weakness/resistance entries use Type and Value, empty immunity and ritual
  states are explicit, and creature abilities have an optional Effect field.
  Existing source fields remain intact and the rendered stat-block information
  is preserved through generated editor mirrors and a compatibility migration.
- Automated baseline: the public ORC/OGL packs, package definitions, creature
  links and spellcasting, area templates, and maintained UI regressions pass
  through `python3 tools/eplus_dev.py check --json`.
- Native-app verification still required: import `dist/test/pf2e-remaster.system`
  and confirm a creature's rendered stat block is unchanged while Special
  Senses, Items, Immunities, Rituals, Lore, Recall Knowledge, and the optional
  ability Effect field can be edited through their new controls. In particular,
  verify the Item reference search, item quantity, the empty Immunities `None`
  row, the empty Rituals `New Entry` row, Recall Knowledge values, Lore inside
  Skills, and Type/Value labels for weakness and resistance entries.
- Current product priority: continue the complete data audit and review upstream
  Encounter+ compatibility before releases. See `ROADMAP.md` for accepted,
  deferred, and completed feature decisions.

Update this file at a material handoff, app-test result, upstream merge, or
release. Do not use it as a chronological work log.
