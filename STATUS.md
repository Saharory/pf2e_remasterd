# Current status

Last updated: 2026-10-04

- Branch: `remaster-community-base`
- Package version: `0.9.0` (pushed; release not yet published)
- Latest completed local work: the creature editor now exposes lossless,
  structured controls for special senses, searchable inventory items and
  quantities, immunity references/custom text, and ritual lists. Named Lore is
  edited inside the same Skills page, Recall Knowledge binds its complete
  knowledge-to-skill pairs, language and special-save notes have clear labels,
  weakness/resistance entries use Type and Value, empty immunity and ritual
  states are explicit, and creature abilities have an optional Effect field.
  Existing source fields remain intact and the rendered stat-block information
  is preserved through generated editor mirrors and a compatibility migration.
  The Skills editor is nested in a valid Encounter+ group section, fixing the
  `sections[4].type` decoding error seen when opening Edit Creature, and its
  nested skill-map control now uses the same valid grouping. Creature ability
  editors separate source-backed Description, Trigger, and Effect fields while
  retaining the original text as a compatibility fallback; Trigger remains
  optional because both reactions and free actions can use it.
- Automated baseline: the public ORC/OGL packs, package definitions, creature
  links and spellcasting, area templates, and maintained UI regressions pass
  through `python3 tools/eplus_dev.py check --json`.
- Spell editor compatibility: fixed the nested area-size input that caused
  `sections[3].fields[8].form.sections[1].type` to reject `decimal`. Size is now
  a decimal field in a group, with native feet conversion in its editor and
  summary. Source checks validate section and field types recursively across
  every form and partial, including tabs, list editors, and field containers.
  The 308 configured spell areas and all published spell records are unchanged;
  this definition-only repair applies to existing/custom spells without a data
  migration. The new asset conversion and timed self/target loading remain
  deferred until the developer confirms the updated app's loading format.
- Spell verification: full source checks pass and the test archive includes the
  corrected editor. Native Edit Spell, area-size editing/saving, and area loading
  still need verification in the updated app: app inspection stalled and macOS
  denied installed-system reads. Check Fireball, Detect Magic, and Bless, and
  confirm creature spell links open their full records. Timed self/target effects
  and expiry are pending the deferred loading upgrade.
- Native-app verification still required: import `dist/test/pf2e-remaster.system`
  and confirm Edit Creature opens without a decoding error, that Skills opens
  with its values and named Lore, and that a creature's rendered stat block is
  unchanged while Special
  Senses, Items, Immunities, Rituals, Lore, Recall Knowledge, and the optional
  ability Trigger and Effect fields can be edited through their new controls.
  In particular,
  verify the Item reference search, item quantity, the empty Immunities `None`
  row, the empty Rituals `New Entry` row, Recall Knowledge values, Lore inside
  Skills, and Type/Value labels for weakness and resistance entries.
- Current product priority: continue the complete data audit and review upstream
  Encounter+ compatibility before releases. See `ROADMAP.md` for accepted,
  deferred, and completed feature decisions.

Update this file at a material handoff, app-test result, upstream merge, or
release. Do not use it as a chronological work log.
