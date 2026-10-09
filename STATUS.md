# Current status

Last updated: 2026-10-10

- The previously reported **Trade Death for Life** and **Tree of Life and
  Death** import issues were investigated here on 2026-10-07 after the user
  clarified that structured spell metadata remained in descriptions. The
  shared import repair below is source-complete; the user approved its native
  presentation and subsequent field-edit/save/reopen checks on 2026-10-07.
- Branch: `remaster-community-base`
- Package version: `0.9.01`. The user authorized pushing the completed editor
  work and replacing the main dist package on 2026-10-05. Version changes,
  tags, and release publication have not been requested.
- Requested baseline push completed on 2026-10-05: `4ea2835` is on
  `origin/remaster-community-base`, including the saved editor design roadmap.
  The subsequent editor work is included in the newer user-authorized push.
- Standing user instruction (2026-10-05): always package each completed system
  implementation/fix for testing, even during the native-testing pause. Keep
  only the latest `.system` in `dist/test`; validate the replacement before
  deleting older systems. This supersedes the earlier pause-related package
  delivery restriction and is saved in `AGENTS.md`. Native testing remains
  user-controlled; no agent app automation is authorized.
- Current test package: `dist/test/pf2e-remaster.system`, rebuilt on 2026-10-10
  with the creature, item, and spell editor redesigns and previous system-wide
  refresh repairs, improved attack/casting/usage summaries, and numeric
  spellcasting-input repair, shared ability writing flow, and character tabs.
  It now also includes the named item activation rendering repair and imported
  activation field conversion below, plus imported Craft Requirements and
  their native item-preview rendering repair, native item variant display,
  corrected category visibility syntax, spell description metadata cleanup,
  restored native scalar-list controls for hazards/vehicles/deities,
  live deity previews with clean imported Description and joined table lists,
  multiline Edicts/Anathema, generic ranked cleric-spell labels/links, clear
  reference section labels, custom-only acuity references, and automatic
  standard sense-acuity rule links.
  Archive inspection/CRC/checksums pass; all 200 packaged source files match
  current source. It includes 18,041 records, including 1,404 spells. Version
  remains `0.9.01`. The three older named test systems were removed after the
  replacement passed verification; this is the only `.system` in `dist/test`.
  Companion manifest, summary, and checksums were refreshed.
  SHA-256: `2bdaab036bb5dbe6b62fa43efdd36a4e0047996e35ce5d1d7aacd4a66f4c37e6`.
- Main distribution package: `dist/pf2e-remaster.system` was replaced on
  2026-10-05 with the verified latest test package above, as requested. The
  manifest, release summary, and checksums were replaced alongside it. The
  main and test archives were identical at that point; archive CRC and
  checksums passed. The newer activation/crafting, variant rendering, category,
  spell metadata, scalar-list, and deity display fixes are only in
  the test package, not this main distribution or the previous branch push.
  Version remains `0.9.01`. Distribution artifacts are ignored
  by Git; the branch push carries source changes and documentation.
- Source checks: the canonical `python3 tools/eplus_dev.py check --json` passes
  with 83 definition files and every maintained validator, including 22 ORC
  packs / 17,359 records, 681 OGL records, creature editability/spellcasting,
  spell durations/areas, hazard/vehicle mechanics, and four UI regression files.
  Revalidated on 2026-10-10 with the repaired virtualenv and bundled Node via
  `../tools/project-env python tools/eplus_dev.py check --json`.
- Spell description metadata: source repair complete on 2026-10-07; native
  presentation approved (user: "yea all looks good"). Audit found 503 spells with leading metadata for fields
  already offered in the editor. `tools/spell_editor_data.py` repairs 479 across
  13 ORC/OGL collections, removing represented leading headers and populating
  missing ordinary text fields such as Trigger/Requirements. It also preserves
  links by retaining richer linked text where ordinary fields can carry it.
  Only consecutive known metadata paragraphs at the start are considered;
  effect prose, outcome blocks, heightened rules, IDs, licensing, and source
  records otherwise remain intact. Unknown metadata (Patron Theme, Deity,
  Domain, Mystery, legacy version notices) stays in the description. Conflicting
  populated values, repeated/inline headers, unmapped areas, qualified geometry,
  unsupported Defense AC, and linked defense/duration/area text remain printed
  rather than losing information or changing native parsing.
  Both full builders call the shared converter after link deduplication; its
  post-link CLI updates only owned spell collections, preserving enrichment.
  The reported Tree of Life and Death now starts with its actual effect;
  Trade Death for Life retains Patron Theme but removes duplicate Range/Target/
  Defense/Duration. Missing reaction triggers such as Blastback's populate the
  Casting details field. Corpus comparison proves all effect/heightened body
  text and internal link routes preserved, and all native timers/map templates
  unchanged. Conversion is idempotent. Ten added conversion cases pass (40
  total), as does the canonical check (83 definitions, nine validators).
  The verified test archive changes only `spells.json` from its predecessor:
  479 of 1,404 spells change, all 18,041 records remain, every other packaged
  file is identical, CRC/checksums pass, and version remains `0.9.01`.
  No user-record migration, version change, push, or publication was performed.
  The user approved the requested presentation checks: fresh Trade Death for
  Life / Tree of Life and Death show mapped metadata once with effect rules
  intact, and Blastback's Trigger appears in Casting details. The subsequent
  Trade Death for Life test also passes: edited Range, Defense, and printed
  Duration display correctly and persist after save/reopen without old
  description headers returning. Old personal copies may retain old data.
- Spell editor efficiency: source complete, native verification pending.
  Type/rank/rarity/traits now share the opening group. **Casting** keeps
  variable action selection and traditions direct, with casting notes,
  requirements, cost, and trigger in a root-context **Casting details** editor
  whose summary shows populated values. **Range & effect** keeps range, printed
  area, targets, defense, and printed duration direct. **Map & token effects**
  groups the existing template/timer links without adding a navigation level.
  Unconfigured casting details and map templates show localized **None**.
  All 21 controls retain their storage paths, input/picker types, visibility,
  defaults, and units. English/French labels are included; spell-area/duration
  and creature-editability checks pass, as does the canonical check. Records,
  migrations, native loading, and versions are unchanged. Item editor source
  work is now complete as described below.
  Casting details native checks pass on 2026-10-07: fill notes, requirements,
  cost, and trigger; summary/displayed spell text and save/reopen; clear all
  fields and confirm clearing persists. The user reports "it works".
  Casting notes is the original free-text `data.cast` field, displayed as Cast;
  imports retain printed timing/action wording here (e.g. 1 minute, Two Actions),
  while `data.castActions` separately supplies the action selections/icons.
  Direct Range/Defense/printed Duration edits, display, and save/reopen pass on
  2026-10-07, including absence of stale description headers.
  Multiple Cast actions also pass on 2026-10-07: Heal test copy retains 1/2/3
  selections and displayed icons after save/reopen; removing one preserves the
  remaining two after save/reopen.
  Area-template/numeric-expiry settings also pass on 2026-10-07: Fireball test
  copy Cone / 12.5 ft and Time / 2 rounds, summaries and save/reopen; printed
  Area/Duration remain unchanged.
  Map placement/loading also passes on 2026-10-07 with no token selected:
  stock Fireball 20-ft-radius area, Detect Magic 30-ft-radius area, and edited
  Fireball Cone / 12.5 ft all place/remove with expected geometry.
  Newly created custom manual spell loading also passes on 2026-10-07: empty
  Area template, Until Dispelled, save/reopen, load onto a test token, no
  countdown, persistence through two rounds, and manual removal.
  Pending functional checks: check an older custom spell with prose in
  `data.duration`. Keep redraw, persistence, and rendered content results distinct.
- Item editor efficiency: source complete, user approved on 2026-10-05.
  The user reports no issues and much better organization. Individual
  save/reopen checks below were not separately reported.
  Category/level/rarity/traits/subcategory share the opening group. Price,
  usage, bulk, description, and category-specific equipment stats remain
  direct. Ammunition, onset, and crafting requirements share a root-context
  **Additional details** editor with a populated summary or localized **None**;
  it remains accessible for empty/custom items of every category. Equipment
  sections also expose populated exceptional properties after category changes,
  preserving zero-valued numeric stats. **Primary activation** edits the original
  `data.activation` fields; **Additional activations** keeps the separate named
  list at `data.activations`. Both remain available when empty. The primary
  summary now includes traits. The original `data.types` list is labeled
  **Variants**, with its entry schema unchanged. Top-level sections decrease
  from 12 to 10 and typical non-category rows from 15 to 13. All 38 bound
  controls preserve paths, input types, defaults, and units. English/French
  labels, focused editability regression, and canonical source checks pass.
  No content, migration, stat-block, or version changes were required.
  Additional details native tests pass on 2026-10-07: filling ammunition/onset,
  summary/displayed text and save/reopen, then clearing both and Craft
  Requirements and confirming they stay cleared after save/reopen.
  Primary activation native tests also pass on 2026-10-07: populate action,
  trait, and text; summary/display and save/reopen; clear those fields and
  save/reopen while named Review/Extra Credit remain unchanged throughout.
  Variant native checks also pass on 2026-10-07: all six fields display, the
  label says Variant, save/reopen and deletion persist, and activations remain
  unchanged. Category-change populated-property retention also passes on
  2026-10-07. Empty-category field visibility and immediate switching for new
  gear/armor/shield/weapon items also pass on 2026-10-10.
  No agent app automation is authorized. The user selected creatures next,
  ahead of shared abilities. The shared ability editor is now implemented as
  described below.
- Deity display repair: source complete on 2026-10-07; native confirmation
  pending. Native preview previously rendered the imported `descr` snapshot,
  so structured edits could not update it; HTML rendered current fields but
  ignored custom Description. Both now render current deity mechanics and show
  custom descriptions when they differ from the original import summary.
  Latest native feedback found the summary still present inside Description,
  and table values/separators stacked because each value passed through `md`
  separately. The converter now clears Description only when it exactly equals
  the import summary; all 420 stock descriptions are empty, and custom text is
  preserved. HTML table cells render the joined values through one Markdown
  block, keeping links and separators on the same paragraph. The user confirms
  the clean Description/table layout now looks good. Remaining deity functional
  checks must still be recorded separately.
  Native uses the new `deity-stats.md` partial; HTML retains its existing table.
  `tools/deity_editor_data.py` derives per-value reference caches from the
  existing linked summary. Views use a cached link only when the live value
  matches and render edited/new values directly, avoiding stale rules. All 420
  stock deities in four collections are enriched by the shared full-builder /
  post-link pass; IDs, licensing, description snapshots, and original fields
  remain unchanged except The Tides of Chaos's legacy cleric-spell dictionary,
  converted to a string list preserving each rank and spell. All 4,428 original
  reference occurrences retain their routes; comparison finds no metadata-word
  loss. Older personal copies without
  reference caches retain their legacy native display to preserve original
  links; no active user-record migration is included. New custom deities use
  live fields and custom Description directly.
  User-requested follow-up completed on 2026-10-10: one two-line multiline box
  for each whole Edicts/Anathema section. Imported values and original links
  seed `data.edictsText` / `data.anathemaText`; original arrays stay intact for
  compatibility. Both views prefer the text form, including empty/cleared text,
  so old values do not reappear. Older saved copies without text fields keep
  their existing list controls; fresh imports/new records use the larger boxes.
  Cleric spells now use a shared ordinal formatter for every explicit supplied
  rank (1st/2nd/3rd/4th/etc.), including dictionary and list inputs. Ranks are
  never inferred from a spell's base rank. Missing links resolve against the
  published spell catalog, preferring core references; no deity/name-specific
  patch. The Tides of Chaos's 1st Ill Omen / 2nd Invisibility / 5th Subconscious
  Suggestion matches both the structured source and local Foundry ORC record
  `../foundry-pf2e/packs/pf2e/deities/covenants/the-tides-of-chaos.json` (Shining
  Kingdoms, p.23). Its three entries now link to the corresponding core spells.
  The user approved the latest layout/presentation on 2026-10-10 ("looks good").
  This confirms the multiline/ordinal appearance. On 2026-10-10, editing both
  directive boxes initially appeared to lose the first edit in either order.
  The user narrowed this down: single-letter edits / pasted replacements fail,
  while making more than one input persists both boxes after saving/reopening.
  This resembles the earlier native text-save bug; app causation is not yet
  independently confirmed for this recurrence. It is not evidence that the two
  distinct field paths overwrite each other. A proposed separate-page workaround
  was withdrawn before packaging; the approved inline boxes remain unchanged.
  Multiple-input persistence passes. The user then confirmed all three requested
  follow-up checks on 2026-10-10: clearing a directive remains empty after
  save/reopen, custom Description displays, and all three Tides spell links open
  the correct spells. Small-edit persistence remains unresolved; original
  weapon/domain link-opening was not included in this three-check confirmation.
  Eight deity conversion cases pass (48 total); focused editability and canonical
  checks pass (83 definitions, nine validators). Verified latest test package
  changes `deities.json` and the two deity views, adding only the new partial;
  The subsequent verified test archive changes only `deities.json` (duplicate
  Description clearing) and `views/deity.html` (joined cell rendering); all
  other data and files remain identical. Latest verified archive changes only
  `deities.json`, `forms/deity.json`, `views/deity.html`, and `deity-stats.md`
  for multiline directives and ordinal/catalog links. All 200 source files match,
  CRC/checksums pass, 18,041 records remain, version is `0.9.01`. No push/release.
  Deity follow-up: original weapon/domain links still need explicit native
  confirmation. Existing saved copies keep their old description text; no
  active user-record migration is included. Do not repeat passed directive
  clearing, custom Description, Tides spell links, or approved visual layout.
  Source-completeness follow-up: comparison with the local Foundry record also
  indicates missing non-spell Tides metadata in the structured import (concerns,
  directives, divine attributes, favored weapon, sanctification options).
  Investigate that source mapping separately; it is not a native control bug
  and was not changed by this editor/rank repair.
- Scalar-list regression: source repair complete on 2026-10-07; the hazard /
  vehicle native retest passes (user: "all good"). The user reported imported immunities visible in the parent summary
  but an empty inner list before editing. Published hazard/vehicle data is
  present and contains plain strings (21 populated hazards / 62 vehicles).
  The earlier refresh workaround incorrectly treated scalar text lists as
  record-list sections. Restore native field-level `type: list` controls at
  `data.immunities` for hazards/vehicles and the eight analogous deity lists.
  This matches the upstream PF2E scalar-list pattern; structured creature
  immunity/weakness/resistance lists retain their working form/row controls.
  All stored control paths and imported records remain unchanged; no migration
  is needed. The maintained refresh guard now distinguishes scalar fields from
  record sections and rejects bare scalar section lists. Hazard/vehicle tests
  verify native control shape against published string entries. Focused checks
  and the canonical check pass (83 definitions, nine validators).
  The verified package changes only `forms/hazard.json`, `forms/vehicle.json`,
  and `forms/deity.json`; all 18,041 records and other packaged files are
  identical. CRC/checksums pass, version stays `0.9.01`, no push/publication.
  The user confirms existing hazard/vehicle immunities populate internally,
  add/edit/delete updates summary/display, and changes/deletion persist through
  save/reopen. Deity scalar lists remain covered by the next deity test above.
- Named item activation rendering: source repair completed on 2026-10-05;
  imported named-entry editing/rendering, save/reopen, and deletion passed on
  2026-10-07. Inspection before the activation test found
  that the shared editor writes `description`, `trigger`, `effect`, and
  `reference`, but the item display rendered only legacy `text`. Both HTML and
  native item views now use the same activation partial in the loop's row
  context. It renders all seven editable ability fields, preserves shared
  Trigger/Description ordering flags, falls back to legacy text when structured
  fields are empty, retains legacy components, and wraps reference destinations
  safely. Native action icon routes now match the existing lower-case folder.
  No form, storage path, record, migration, or version changed. The maintained
  editability regression covers this previously missing rendering contract;
  focused and canonical checks pass (83 definitions, nine validators).
  Verified replacement test archive changes only `views/item.html`,
  `views/item.json`, and `views/partials/item-activation.md`; all other entries
  and all 18,041 records are unchanged. CRC, checksums, and 199 packaged source
  files match. The imported-item test below confirms structured named rules,
  save/reopen, deletion, and preservation of the other named entry. Independent
  primary activation editing/clearing now also passes in the follow-up test.
  App update results are tracked
  separately below. This repair is
  committed locally only; no push or release publication was performed.
- Imported item activation conversion: source complete on 2026-10-06;
  native presentation and the requested follow-up checks passed on 2026-10-07.
  The user confirms that the complaint concerns
  existing imported text, not new editor input. Audit found 2,661 items mention
  Activate in general `descr`, with no structured activation data. The new
  deterministic `tools/item_editor_data.py` pass recognizes explicit headings
  and populates 2,653 items across 20 ORC/OGL item collections: 1,873 primary
  activations and 1,162 additional entries. It preserves general prose,
  crafting/shield properties, and variant sections. Only root activations and
  exact-name variant activations are assigned to the current item; ambiguous
  or incidental mentions remain intact. Equipment-header activations supply
  actions/traits without guessing that all following prose is their Effect.
  Timed/variable costs remain readable in description text instead of acquiring
  a guessed fixed action cost. Named rules use the shared Trigger/Description /
  Effect parser and retain their legacy body. Activation trait links remain
  clickable in both renderers. Existing/cleared explicit settings are preserved.
  Full builders invoke the same converter; the activation-only CLI runs after
  public link enrichment so unrelated linked records are not regenerated.
  Reference-table rebuilding also reads activation-owned text; table IDs and
  outcomes are unchanged. Tests cover scope, timing, coexistence, idempotence,
  source rules/links, and compatibility. Corpus comparisons prove item IDs,
  licenses, other data, all non-item collections, and tables unchanged; only
  the owned activation fields/description spans changed. All 24 conversion
  tests and the canonical check pass (83 definitions, nine validators).
  The verified test archive changes only `items.json` and the two activation
  display partials; 199 packaged source files match, CRC/checksums pass, and
  all 18,041 records remain. Version stays `0.9.01`; no push/publication or
  active user-record migration. Fresh stock items get converted fields;
  older personal copies may retain their pre-conversion data.
  The user approved the imported activation presentation in the current test
  package, then reported "all good" for editing Review's Effect on a test copy
  of Accolade Robe, save/reopen/displayed rules, adding/deleting a temporary
  named activation, and preservation of Extra Credit. Those checks are passed;
  do not repeat them without a new regression.
- Item Craft Requirements: source repair complete and requested native checks
  passed on 2026-10-07 (user: "works well now"). The user clarifies that the Additional details text
  box is present and saves, but the item preview omits the saved text. The
  native `views/item.json` lacked this field; the HTML template already renders
  it. Native display now includes the saved field and its label, with regression
  coverage guarding both display modes. A separate import gap left requirements
  in `descr`: 532 items contain explicit labels, none had the structured field.
  The deterministic item-editor converter now populates `data.craftRequirements`
  for 530 items in 14 ORC/OGL collections. Two records contain only other-variant
  requirements and remain untouched. Root/exact-name variant requirements are
  moved without guessing; following headings, dividers, properties, other
  variants, and general notes stay in the description. Explicit/cleared GM
  crafting settings and existing activation fields are preserved. Full ORC/OGL
  builders and the post-link enrichment CLI share this conversion.
  Comparison with the pre-conversion corpus proves every rule token and link
  preserved, with only owned description/requirement fields changed. Six added
  conversion cases pass (30 total), as does the canonical check (83 definitions,
  nine validators). The validated test archive changes only `items.json` and
  `views/item.json` from its predecessor; all 199 packaged source files match,
  CRC/checksums pass, and all 18,041 records remain. Version stays `0.9.01`.
  The user confirms the requested fresh-item populated field, edit/save/reopen,
  and displayed-text test works after importing the rebuilt package. Do not
  repeat that test without a new regression. The user also confirms clearing
  the field persists after save/reopen in the follow-up Additional details test.
  Older personal copies may retain their previous description-only data.
  Ammunition/onset filling, summary/display, save/reopen, and clearing also pass.
- Item variant display: source repair complete on 2026-10-07; the user confirms
  all six variant values display, including level zero. The remaining label,
  save/reopen, deletion, and activation independence checks also pass in the
  user's follow-up. Preparation for the next verification found native `views/item.json`
  omitted the editable `data.types` list, while HTML already rendered it.
  The native view now uses the existing `item-type.md` partial with each variant
  as its context, matching HTML. The shared partial also preserves level zero
  instead of treating it as an absent value. The maintained editability suite
  guards both display routes and all six editable variant fields. Canonical
  checks pass (83 definitions, nine validators). The verified latest test
  archive changes only `views/item.json` and `views/partials/item-type.md`;
  all content, forms, and stored data remain unchanged. CRC/checksums and all
  199 source files match. Version remains `0.9.01`; no push/publication.
  Native feedback also identified the old shared display label "Type" instead
  of "Variant". The shared partial now uses the existing localized
  `Item.Variant` label (English Variant / French Variante), aligning HTML and
  native views with the editor. No data or form binding changes. Canonical
  checks pass; the rebuilt test archive changes only `item-type.md` from its
  predecessor. CRC/checksums pass; all other packaged files are unchanged.
  All requested variant checks are now passed; do not repeat without a new
  regression.
- Item category visibility: source repair complete on 2026-10-07; the user
  confirms populated values retained after changing category and save/reopen
  ("yea it retained"). On 2026-10-10, the user confirms all requested blank-item
  category checks pass: Armor AC/Dexterity cap, Shield Hardness/HP/Broken
  Threshold, Weapon Damage/Range/Hands, and Adventuring Gear Hands appear
  immediately when switching category. Preparation found unsupported `elsif` tags in the
  Armor and Adventuring Gear visibility conditions. These now use supported
  `elif`, as in official 5e templates. Conditions, controls, and stored paths
  otherwise remain identical. The maintained editability suite now rejects
  this unsupported tag in item forms. Canonical checks pass (83 definitions,
  nine validators). The verified test archive changes only `forms/item.json`;
  content and every other packaged file remain unchanged. CRC/checksums pass,
  version remains `0.9.01`, and no push/publication occurred.
  The requested retention test used armor AC 2/Dex Cap 0 changed to Adventuring
  Gear and gear Hands 2 changed to Consumable, followed by save/reopen.
  The user's confirmation covers retention; do not repeat it without a new
  regression. The separate empty-item category-switch field-appearance check
  was not explicitly reported.
- Creature editor efficiency: source complete, user tests pass on 2026-10-05.
  The user approved the four-tab layout and explicitly reported all tests
  passing. This native pass covers the layout/refresh iteration delivered in
  package SHA-256 `3a94378992e3f12f740c09a3cbfae84f97613e75f386659f7c9329dc5b88377b`;
  new summary rendering is a separate pending check below.
  Four native tabs organize the existing editors: **Identity** holds combined
  level/rarity/size/traits, Recall Knowledge, inventory, and interaction
  abilities; **Statistics** holds perception, senses, Skills/Lore, Speed,
  attribute modifiers, and languages/notes; **Defenses** holds AC/HP/hardness
  with explicitly labeled notes, saves/special modifiers, immunities,
  weaknesses/resistances, and automatic/reactive abilities; **Actions & Magic**
  holds attacks, spellcasting, rituals, and offensive/proactive abilities.
  Sections decrease from 18 to 15, at most four per tab. No additional subform
  layer, visibility restriction, or binding scope was introduced. Existing
  Skills/Lore, senses, immunity, weakness/resistance, movement, item, ability,
  attack/damage, spellcasting, and ritual editors remain intact. All 118 resolved
  bound controls, including nested list-entry partials, retain their paths,
  types, defaults, units, visibility, and list metadata in a before/after audit.
  The maintained creature regression now traverses tabs and guards every inline
  attribute, direct ordinary statistics, and all three separate ability lists.
  Focused editability/spellcasting and canonical source checks pass.
  English/French labels are included, and the Ractive typo is corrected.
  Content, migrations, rendering, and native loading are unchanged.
  The previously pending tab navigation, ordinary stats/notes, save/reopen,
  Lore/immunity/weakness/resistance/Speed refresh, inventory, ability-list,
  attack component, and grouped spell/ritual checks are covered by the user's
  reported all-tests pass. No agent app automation is authorized.
- Existing entry summaries: source complete, user reports all tests pass.
  Attack rows now preview type/action cost, signed attack modifier, damage
  components with their original connectors and types/effects, and named
  effects; legacy printed damage and component formulas retain display
  fallbacks. Component rows explicitly show formula plus type/effect.
  Casting previews show DC, signed attack, focus points, and original rank-group
  labels; cleared text values omit their labels while zero remains visible.
  Ritual previews retain DC/rank groups. Spell and ritual group rows
  add at-will and usage/constant notes to their names. Entry rows localize rank
  and at-will labels, retain rank/modifier zero, and omit missing-rank labels.
  Character attack/casting rows use the same summaries; its navigation is
  unchanged. A before/after comparison verifies nine affected/referenced form
  trees preserve controls, bindings, types, defaults, units, visibility,
  picker mappings, and routes. Native if/for tags are balanced in 29 inspected
  row templates. The maintained editability regression guards summary coverage
  and zero-value visibility; focused editability/spellcasting and canonical
  source checks pass.
  Existing structured editors, ability name-only rows, tabs, references,
  content, migrations, stat blocks, and load behavior remain intact. No new
  nested screens were added; weakness/resistance wrappers retain the earlier
  native-confirmed implementation.
  After the numeric-input repair below, the user reports the latest package
  looks good and all tests pass on 2026-10-05. Preserve that reported native
  pass for this summary iteration; do not repeat its analysis or testing
  request. No agent app automation is authorized.
- Spellcasting numeric-input repair (2026-10-05): the user supplied screenshots
  showing **Divine Innate Spells** with DC 37 / attack +29 in the parent preview,
  but **None** in the entry's Spell Attack/DC controls. The user confirms the
  rank groups appear normally. This matches Astradaemon's numeric source data;
  that entry has no focus-point value, so its **None** is expected. The shared
  casting partial inherited text controls for `spellAttack` and `spellDC` from
  the original form, predating today's redesign. Both now use native `number`
  controls, matching the numeric data and existing Focus Points control. All
  paths, rank groups, spell entries, summaries, content, and migrations remain
  unchanged. The maintained casting regression covers the real Astradaemon
  fixture and numeric control types. Focused and canonical source checks pass.
  Native confirmation: the user reports "looks good all pass" after testing
  package SHA-256 `67b2ff91c6bf5404d677e981784ca8a1df1f0a85cfa58283a4cc2692b1b26931`
  on 2026-10-05. The requested value population, edit/save/reopen, and parent
  preview checks pass. This repair is native-confirmed.
- Shared ability writing flow: source complete; user tests pass on 2026-10-05.
  The shared partial now has two groups instead of six: Name, Action cost, and
  Traits first, then **Rules text** with Trigger (optional), Description,
  Effect, and Linked action (optional). Short English/French placeholders
  distinguish activation conditions, context/requirements/passive rules, and
  the effect. All seven bound controls retain their paths, types, attribute
  types, defaults, units, and visibility in a before/after comparison. Trigger
  and Effect stay editable for every action cost and for passive abilities.
  This applies to all three creature ability lists, additional item
  activations, hazards, and vehicles. No binding scope, nested screen, data
  migration, content, summary, rendering, or load behavior changed; original
  trigger-order/paragraph flags and reference links are preserved. The existing
  editability regression covers the seven bindings and source-text fidelity
  and passes, as does the canonical source check.
  The user approved the result ("stunning pass") on 2026-10-05. Preserve this
  native confirmation for package SHA-256
  `3bf4828a1f2b14d5484a115db84dbb4b185e02452df59756c6f29262c5667744`.
- Character navigation: source complete; blank-state layout approved,
  populated-character verification pending.
  Four native tabs replace the continuous 12-section form: **Main** (identity,
  traits, HP, core statistics, movement, resources), **Abilities & Skills**
  (attribute modifiers, saves, skills, attacks), **Inventory**, and **Spells**.
  Uses the same tab containers/icons as the official 5e editor, with English/
  French labels. All 12 original sections and all 63 resolved bound controls
  retain their definitions, paths, types, defaults, summaries, and bindings;
  root-context movement and row-context attack/casting editors are preserved.
  The existing editable inventory text field remains accessible. The focused
  editability regression and canonical source check pass.
  Native feedback (2026-10-05): the user inspected a blank character form
  and said the overall layout looks good. They do not yet have a character
  to test populated records. This confirms the blank-state layout only for
  package SHA-256
  `b30bc9e4fcbcd39efe2e52bebbf5c07d72fcf5dbfee21a6857637ba9fc059618`.
  When a character is available, pending checks are editing a statistic,
  Speed, an attack, inventory text, and casting numeric values, then saving/
  reopening to verify persistence. Existing/populated records remain untested.
  No agent app automation is authorized.
- Recent native feedback (2026-10-05): the user said the spell layout looks
  good apart from Cast actions offering Custom Options, and approved the item
  layout with no issues. The user subsequently approved creature tabs and
  reported all creature tests passing. Cast actions remains unchanged after
  the user aborted the attempted workaround; app picker behavior is deferred
  to another chat.
  This feedback does not confirm the earlier hotfix or a new app version.
- Native testing: user tests on Mac, Encounter+ 5.0.9 (4536), confirmed from
  installed-app metadata on 2026-10-07. The user performs
  all further app tests; do not run agent UI automation or visual app inspection.
  Analyze an attached image/recording only when explicitly requested.
- App update confirmed on 2026-10-07: the user reports the app was updated and
  all save-issue bugs are fixed. Record text persistence as user-confirmed
  fixed after the update; no agent app testing was performed. The user then
  confirmed both requested refresh checks pass: nested Duration selecting Time
  immediately reveals value/unit controls, and Recall Knowledge selection
  checkmarks appear immediately. The previously reported save/refresh bugs are
  now resolved in the user's native tests.
  Binding review: retain the current creature Immunities/Weaknesses/Resistances forms.
  Their list sections still bind to `data.immunityEditor.entries`,
  `data.weaknessEntries`, and `data.resistanceEntries`; row controls remain
  relative to their own entry. Only the outer page's extra object/list scope
  was removed. Resolved storage paths are preserved and guarded by the existing
  regression suite; no technical reason to restore that extra scope was found.
  No source/package change is required by this app update.
- Earlier resumption: native testing resumed by the user on 2026-10-05 despite the hotfix still
  being unavailable. Read-only installed-app metadata still reports 5.0.8
  (4530). Continue the remaining functional verification, documenting known
  selection/redraw/text-save issues separately from content and storage-path
  regressions. The 2026-10-07 update above supersedes the save-issue status.
  No agent app automation. Named activation checks now pass as recorded above;
  primary activation editing also passes. Avoid repeating approved creature
  layout/refresh tests.
- Earlier pause: native testing stopped by the user on 2026-10-04. The user relays that the
  Encounter+ developer confirmed these issues are a bug introduced by the
  recent app update and expects a hotfix later on 2026-10-04. This is a reported
  upstream diagnosis/plan, not confirmation that a fix is released or passes.
  The user subsequently resumed and installed the app update; do not schedule monitoring
  automatically. Package completed system
  changes under the newer standing user instruction above.
  Preserve all existing passes, source checks, and failed-case reproduction.

- Confirmed refresh repair: object-bound nested forms retained stale rows and
  summaries after mutations. Immunities New Entry/Delete reached the editor
  data but required leaving/reopening to redraw, as shown in the user's
  supplied recording. A native-view-only diagnostic did not help; HTML display
  was ruled out for that failure. The next candidate removed the object scope
  from the Skills/Immunities parent forms and qualified their controls through
  the full entity paths. The user confirms that candidate works and explicitly
  requested applying it throughout the system. Treat that as confirmation of
  the tested redraw behavior, not proof of the app's internal cause.
- Earlier system-wide application: 22 nested form pages retained the parent
  context. Movement (Ancestry, Character, Creature), Recall Knowledge, and item
  activation use fully qualified paths. Field-level list pages for creature
  senses/weaknesses/resistances retain explicit form wrappers with root-bound
  record-list sections. Deity lists and hazard/vehicle immunities were also
  wrapped then, but their scalar-list wrappers are now reverted after the
  user-reported empty-inner-list regression above. Skills/Immunities
  retain the confirmed repair; spell Area/Duration already used root context.
  Entry forms remain relative to their own list row, including references and
  quantities. A before/after traversal verified that every resolved storage
  path is identical, including all list-entry paths. No content rebuild or
  migration is needed. The maintained creature suite checks context preservation
  throughout the forms and guards the shared movement/activation/recall paths.
  Skills/Immunities, creature Weaknesses/Resistances, and creature Speed are native-confirmed;
  other extensions need user spot checks.
- Separate text-edit persistence issue, fixed after the app update according to
  the user's 2026-10-07 report. Earlier reproduction: small name edits and selecting existing
  text then pasting a replacement can fail to save. The user reproduced the
  single-character saving failure in official D&D as well. Clearing the text
  first, then pasting, works even if the final name differs by one letter;
  there is no demonstrated minimum edit-size rule. Waiting/focus changes and
  a larger textArea control did not help. Keep normal name controls. This issue
  was not fixed by the system refresh repair. The workaround is retained here
  as historical reproduction; it is no longer required by the latest user result.
- Special senses: the user confirms add/reference selection, Imprecise choice,
  Details editing (30 to 60 feet), statblock link opening, save/reopen, and
  deletion pass on 2026-10-10. First polish package failed its native label
  check: the app ignores `placeholder: Reference` on native reference controls
  and still displays None. Do not record that placeholder change as a pass.
  Latest correction gives all seven existing reference pickers an explicit
  Reference section heading, preserving one-tap picker access. Ineffective
  placeholders were removed. Native empty value may still read None under
  the heading; no undocumented row-text override is claimed.
  The user also requested manual reference selection for custom acuity. A
  Custom Acuity Reference section now exposes the existing `acuityReference`
  only when `acuity` is nonempty and not precise/imprecise/vague. Choose a custom
  value in the native picker and return to the sense editor to access it.
  Standard choices hide this section and automatically link their fixed rule
  from the live acuity in both previews, ahead of stale saved references.
  Hidden custom reference data is retained; Custom Sense Text remains
  authoritative. No content rewrite or save hook was introduced.
  Maintained guards cover live-choice routes, legacy precedence, custom-only
  visibility and visible reference headings. Canonical checks pass (83
  definitions/nine validators); package CRC/checksums and all 200 source
  matches pass. Latest archive changes only seven form partials; all 18,041
  records and views remain byte-identical to the preceding test archive.
  Version remains 0.9.01; latest test package rebuilt, no push or release.
  Next native check: visible Reference heading, custom acuity reference
  selection/save/reopen/link, and hiding the custom-reference section when
  switching to each standard acuity (whose link follows the new choice).
- Creature editor: lossless structured controls expose special senses, inventory
  item references/quantities, immunity references/custom text, rituals, named
  Lore inside Skills, and Recall Knowledge subject/skill pairs. Language and
  special-save notes are labeled, defenses use Type/Value, and abilities expose
  Description, optional Trigger, and Effect while retaining source compatibility.
  Existing source fields remain intact through generated mirrors. The earlier
  Skills section decoding error is fixed; native Edit Creature/Skills opens.
  Confirmed user passes: Lore modifier persistence, Items quantity editing,
  Items/Immunities removal through Mac's Copy/Delete context menu, and Resilient
  Form Effect editing, save/reopen, and stat-block rendering with Trigger intact.
  The user also confirms the complete Weaknesses/Resistances test: New Entry
  appears immediately, type/value edits update on return to the list, saved
  values persist and render in the stat block, and context-menu deletion
  redraws immediately and remains deleted after saving/reopening.
  Creature Speed also passes: Walk/Fly editing, immediate summary updates,
  save/reopen, and stat-block rendering. Before the app update, Recall Knowledge deletion worked, but
  subject/skill picker checkmarks appear only after leaving/re-entering Recall
  Knowledge, so selection feedback fails. Its entry controls correctly use the
  row-relative `subject` / `skills` paths, a standard pattern also used by 5e
  list-entry forms. No binding error was identified. The user confirmed
  immediate selection checkmarks after the 5.0.9 update on 2026-10-07.
  Recall Knowledge DC/stat-block/save verification is not yet
  confirmed; do not mark the whole Recall Knowledge test passed.
- Reference repair: native selections can include source-name spaces, e.g.
  `/item/chest-player-core/player core`. All nine dynamic creature Markdown
  destinations now use angle wrappers, preserving valid links with spaces or
  parentheses. Foundation Markdown checks and the maintained regression pass.
  The user confirms Chest renders correctly and opens the expected item.
  Other editor reference types still need native verification.

- Spell editor compatibility: the nested area-size input is a decimal field
  inside a valid group, with native feet conversion in the editor and summary.
  Source checks recursively validate native section/field types. This fixes the
  earlier area-form decoder error without changing stored spell data.
- Spell loading: all 1,404 spells preserve printed prose in `data.durationText`.
  Native duration descriptors configure 809 clear timers/next-turn endings;
  595 spells load as manually removed reminders with only
  `data.durationUnit: "round"`, no value or expiry type. Read-only inspection
  of the installed loader established support for that unit-only descriptor.
  Sustained durations supply a maximum timer, not automatic Sustain. The 308
  map-area templates remain intact; deferred upstream conversion is unchanged.
- Duration regression: nested Time expansion now passes after the app update,
  confirmed by the user on 2026-10-07. Earlier specific result: readable spell
  and status-effect duration names after restoring explicit option maps; the
  other requested duration checks pass (save/reopen and preview). Only Spell
  Time still requires leaving/reopening before value/unit controls appear.
  The native status-effect editor expands immediately. The rejected field-picker
  candidate added navigation; retain inline choices and expanding controls.
- D&D comparison and current regular package: the installed `dnd5e.system` and local
  `../dnd5e-source/forms/spell.json` use an unbound parent form, full entity
  paths, package-declared picker maps in `types.json`, and a full template
  returning `true` for visible timer sections. PF2E already shares the context
  pattern; it had removed its own duration maps and used bare visibility
  comparisons. Restore the complete `DurationType` / `DurationUnit` maps (also
  present in `../upstream-pf2e/types.json`) and use
  `{% if data.durationType == 'time' %}true{% endif %}` for both timer sections.
  Stored native values stay identical. Ordering lists all seven native types
  and four units. English/French labels, singular/plural summaries, None/reset,
  and parent help remain intact. No additional picker screens or controls.
  D&D also shows timer controls for an unset type, so this comparison does not
  prove PF2E's live Time transition. Source checks guard complete option maps,
  labels, ordering, layout, and storage. The user confirms the option-map repair,
  but matching the visibility template did not repair live Time expansion.
  The user also confirms that official 5e Instantaneous to Concentration
  requires leaving/re-entering its Duration page before timer controls appear.
  The same failure is therefore reproduced in an official system; distinguish
  this shared conditional-form refresh issue from the fixed PF2E option labels.
  The explicit option-map repair is native-confirmed; its visibility-template
  change did not fix the nested page. See the new partial candidate below.
- Native status-duration inspection: the working editor is app-owned. PF2E's
  `forms/status-effect.json` adds stage/rarity/traits/printed duration; it does
  not define the expiry picker or expanding timer controls. The bundled 5e
  archive has no corresponding status-effect duration form. Read-only Swift
  metadata inspection of the installed app identifies a separate `DurationForm`
  with `_duration`, `_durationUnit`, and `_durationType` properties, alongside
  `StatusEffectForm`. Generic custom editors instead use `EntityEmbeddedForm`
  and `EntityFormSection` with a definition and `_data`. This confirms separate
  components, not the internal cause of the missed redraw. The public
  [FormDefinition schema](https://docs.encounter.plus/reference/schema/form-definition/)
  exposes no duration field or hook to embed/call `DurationForm`. No supported
  way to reuse that native page in a spell's JSON form was found. Do not invent
  unsupported refresh keys or claim the native component was copied/fixed.
- Confirmed root-form diagnostic: `dist/test/pf2e-remaster-duration-root-test.system`
  temporarily moves the same three duration sections directly into the main
  Spell form. It changes only `forms/spell.json` in the regular archive, keeps
  the same stored paths/labels/visibility expressions, and remains `0.9.01`.
  Source: `dist/test/diagnostics/spell-duration-root-form.json`; native form
  definition validation passes. SHA-256:
  `479a20798aae760aad8c9479a5902ee7cc8596b471258c8f38713c8656bac157`.
  The user confirms immediate Time expansion works there, and asks why the
  controls moved out of their section. The move was only to isolate the nested
  page. Do not adopt that main-page layout as the final design or repeat this
  confirmed test. The regular source retains the dedicated Duration page.
- Failed duration-page candidate: move its existing three sections to
  `forms/partials/spell-effect-duration.json` and reference that partial from
  the unbound parent form, matching the confirmed Skills/Immunities pattern.
  Resolving this partial exactly reproduces the previous JSON definition:
  layout, labels, conditions, summaries, and every stored path are identical.
  Read-only app metadata distinguishes `EntityPartialForm` (own model and
  form data) from `EntityEmbeddedForm` (definition and data). This supports
  testing a partial page; it does not establish which route the app selects
  or prove the redraw is fixed. The spell suite checks the dedicated partial
  route and all existing duration behavior. Focused and canonical checks pass
  (83 definitions, nine validators). The rebuilt archive adds only the new
  partial and changes `forms/spell.json`; every other entry is identical.
  Last result before the app update: it still requires leaving/re-entering to reveal Time
  controls. A partial reference does not avoid the missed redraw. Do not repeat
  this candidate or claim that the dedicated page now works. The main-page
  diagnostic remains the only confirmed immediate Time expansion.
- Duration-field decision: the user explicitly chose to keep printed duration
  and token expiry separate after the feasibility report. Do not consolidate.
  Audited all 1,404 spells: 694 plain timers, 56 turn-relative endings, 59 timed
  descriptions with additional wording, and 595 manual reminders covering 22
  distinct descriptions (including empty). The native value/type/unit fields
  alone are lossy: Haste's `1 minute` and Buzzing Bites' `sustained up to 1 minute`
  both store the same 1-minute timer; Mystic Armor's `until your next daily
  preparations` and Restyle's `unlimited` both store the same unit-only manual
  reminder. `data.durationText` retains the full descriptions. Do not delete or
  silently replace source duration prose. No consolidation was implemented.
- Earlier nested Time refresh disposition, before app 5.0.9: no reliable package fix preserving the
  existing dedicated page has been found. Keep that layout and use leaving /
  reopening as the workaround. The user accepts waiting for the Encounter+
  developer if this cannot be solved here; do not send further speculative
  packages or repeat the confirmed experiments. The local developer report
  is `NATIVE-FORM-REFRESH.md`, with exact steps, official 5e reproduction,
  passing controls, and a bounded inference about nested section invalidation.
  Nothing has been submitted or sent externally. Continue other verification
  independently. This issue is now resolved in the user's 5.0.9 native retest
  recorded above; no release approval has been given.
- Existing/custom spell migration: `migrations/0.9.02.js` is prepared and tested
  against all 1,404 durations; it preserves prose and GM settings and is
  idempotent. It remains inactive while the package is `0.9.01`. Legacy duration
  prose remains readable/editable, and previously converted spells with empty
  settings gain a manual descriptor when the future migration runs.
- Confirmed native spell passes: Haste's 1-minute timer; Shield's expiry at the
  start of the loaded token's next turn; Command surviving through the target's
  next turn and expiring at its end; Heal/Mystic Armor without countdowns,
  persisting through several turns, and manual removal. Switching a timer to
  manual persists and behaves correctly, although its preview was stale before
  the display/refresh changes. No-token map loading/placement/removal now passes
  for stock Fireball / Detect Magic and the modified fractional cone.
  Distinct caster/source assignment also passes on 2026-10-07: effect loaded
  onto B with Source A survives B's turn and expires at A's next turn start
  for Source Start Next Turn; Target End Next Turn expires at B's next turn
  end while Source remains A.

- After the confirmed 5.0.9 (4536) update: save issues are user-confirmed fixed.
  Nested Duration Time expansion and Recall Knowledge selection checkmarks
  also pass in the user's follow-up. Do not repeat these resolved cases without
  a new regression. Craft Requirements import/edit/save/display also passes.
  Additional details ammunition/onset and clearing checks also pass.
  Primary activation editing/clearing and named-entry independence also pass.
  All requested item variant checks also pass.
  Item populated-property retention after category changes passes.
  Spell Casting details fill/display/save/reopen/clear also passes.
  Imported spell metadata presentation also passes.
  Direct spell Range/Defense/printed Duration edits also pass.
  Multiple Cast actions selections/icons/save/reopen/removal also pass.
  Area-template/numeric-expiry settings and printed-field independence pass.
  No-token map placement/loading/removal with stock/fractional geometry passes.
  Distinct caster/source and target-relative expiry also pass.
  New custom spell manual loading also passes.
  Hazard/vehicle immunity population/add/edit/delete/display/save also passes.
  Deity directive clearing, custom Description display, and all three Tides
  spell links also pass on 2026-10-10. Small-edit saving remains unresolved.
  Empty-item category field visibility/immediate switching also passes on
  2026-10-10. Special-sense mechanics also pass.
  Next focused test: reference placeholders and automatic acuity links above. Remaining deity
  checks include original weapon/domain links. Verify redraw and save/reopen;
  source checks alone do not establish native passes. Remaining
  earlier coverage: empty Immunities/Rituals,
  ritual links and creature spell links. Avoid repeating confirmed
  passes unless a new regression or scope change warrants it.
- Current product priority: continue the complete data audit and review upstream
  compatibility before releases. See `ROADMAP.md` for product decisions.

Update this file at a material handoff, app-test result, upstream merge, or
release. Do not use it as a chronological work log.
