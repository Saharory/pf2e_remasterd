# PF2E Remaster and Web Client Roadmap

Last reviewed: 2026-10-05

This is the decision record for work discovered while comparing the PF2E
system and community web client with the official Encounter+ repositories,
especially the [official 5e system](https://github.com/encounterplus/dnd5e),
[Module Packer](https://github.com/encounterplus/module-packer), the older app
source, support tools, and the current web client.

## Confirmed next work

### 1. Genuine rollable tables — complete

The 24 PF2E tables already in the system are sourced **reference/look-up
tables**. They do not roll a random result. Encounter+'s native `Table` entity
and Module Packer also support actual roll tables whose rows cover dice ranges.
The official 5e system ships many examples.

The PF2E implementation should:

- use native Encounter+ table records and dice ranges;
- produce a one-click random result rather than merely displaying rows;
- give every table a clear source, book, and page when a page is known;
- use only content whose distribution is permitted by the relevant license;
- include only true dice-result tables, not every static look-up table;
- expose the useful set through a compact Operations Center page.

Implementation status: 30 licensed, source-backed tables now use Encounter+'s
native roller. The Operations Center has a compact Random Tables page grouped
by use, with contextual shortcuts from hexploration, crafting, and treasure.
The page is included automatically in the A–Z index. The expanded set was
app-tested and published in system version 1.701.9.

Existing DC, encounter-budget, creature-building, treasure-by-level, cover,
detection, and counteract tables remain reference tables because they are not
random outcomes.

### 2. Complete data audit

Continue auditing all entity families, not only hazards and vehicles, for:

- complete mechanics rather than abbreviated imports;
- book-like field order and readable HTML views;
- source book and page, or the book alone when no reliable page is available;
- GP price/value where the source supplies one;
- working internal links for referenced conditions, actions, traits, spells,
  items, and rules;
- current errata and Remaster wording;
- correct licensing and attribution for each source pack.

Hazard and vehicle sheets received this treatment already; that does not prove
that every other entity family is complete.

### 3. Creature spell access — complete

Area-template loading now works for safe, fixed spatial spell entries. The
existing Library search is already a good global spell finder, so do not add a
duplicate launcher. Complete source-derived spellcasting is now included for
685 creatures: 6,145 spell-list entries and 145 rituals preserve their casting
groups, ranks, slots, DCs, attacks, focus points, at-will/constant notes, and
uses. All available spells and rituals link to their full library records and
therefore inherit the existing safe fixed-area load behavior. Six legacy OGL
names whose records are not distributed in the Remaster system remain visible
as plain text instead of opening dead links. Spells without a safe fixed area
receive no forced map template; they can still load an effect onto a selected
token.

### 4. Keep following upstream compatibility work

Continue reviewing official system, package, and web-client changes before
each release. Reuse official migrations, manifest conventions, validation,
and packaging behavior where appropriate instead of maintaining avoidable
fork-only machinery.

### 5. Spell effects — complete

All 1,404 published spells can now create their own native status effect when
loaded onto a selected token. This resolves the spell-effect menu problem:
keep the menu focused on conditions and reusable general effects, including
effects caused by nonmagical attacks. Do not add a separate menu entry for each
spell; load its effect directly from the spell record instead. The user has
confirmed that this workflow meets the intended need.

- The 809 spells with a clear duration use native timers or next-turn endings.
- The remaining 595 spells create manually removed reminders, as agreed.
- Printed duration text remains intact and native effect settings are editable.
- Sustained spells use their stated maximum duration; the GM still handles
  Sustain, early removal, and mechanical modifiers.
- Existing safe area placement remains available without a selected token.
  Map areas do not inherit the token effect's timer; native area expiry is
  deferred below.

### 6. PF2E editor efficiency — approved, spells first

Approved on 2026-10-05. Work through the checklist below one step at a time,
starting with spells. This is the saved design analysis and implementation
reference; consult it before repeating the 5e comparison.

The comparison used the local official 5e forms in `../dnd5e-source/forms/`
and our `forms/`. The main opportunities are context-sensitive fields, useful
summaries, fewer small sections, and navigation by editing task. PF2E needs
more mechanics, but optional details do not all need permanent main-form rows.
These findings come from source definitions; native scrolling, spacing, and
tap behavior have not yet been compared in the app.

**Design rules for every step**

- Keep frequent edits directly accessible. Use native summary subforms for
  optional details only where the reduced clutter justifies another click.
- Show meaningful current values in summaries so users can inspect a record
  without opening every entry. Never hide a populated exceptional field or
  remove the route needed to add it to a new record.
- Preserve all editable mechanics, internal references, storage paths, legacy
  compatibility, variable-action casting, and existing load behavior.
- Printed spell duration and native token expiry remain distinct settings.
  The editor redesign does not add rule automation or map-area timers.
- Reuse native groups, tabs, conditional fields, and existing partials. Keep
  layouts and labels readable at narrow in-app widths.

**Implementation order and saved findings**

- [x] **1. Spells — source complete; native verification pending.**
  Our main form exposes Requirements, Cast, Cost, and Trigger alongside Range,
  Area, Targets, Defense, and Duration. The 5e form uses compact summaries for
  related casting details and conditional fields within those editors.
  Combine identifying fields; keep common spell mechanics directly editable;
  collect optional requirements, casting notes, costs, and triggers under
  **Casting details**. Group Area Template and Token Effect Duration under
  **Map & token effects**, with useful summaries and clear labels. Preserve
  both printed-duration storage variants and numeric token-duration editing.
  Sources: `forms/spell.json`, `forms/partials/spell-effect-duration.json`,
  `views/partials/spell-effect-duration.md`, and
  `../dnd5e-source/forms/spell.json`.
  Implemented on 2026-10-05: combined identity fields, a root-context
  **Casting details** summary/editor, direct **Range & effect** fields, and a
  **Map & token effects** group retaining the existing direct subform links.
  Grouping the map/token links adds no extra editor level. Typical main-form
  rows decrease from 17 to 14; all 21 editable controls retain their original
  bindings, input/picker types, visibility rules, defaults, and units.
  English/French labels and the maintained spell regression were updated.
  Focused checks and the canonical check pass; native checks remain in
  `STATUS.md` while user testing is paused. The pre-redesign baseline was
  pushed to `origin/remaster-community-base` at `4ea2835` before this work.
- [x] **2. Items — source complete; user approved.**
  Armor, shield, weapon, and gear sections already filter by category, but
  Ammunition and Onset appear in the general group for every item. Category
  follows separate rarity, traits, and level sections. Put category and level
  early, combine identity fields, and expose specialized properties when
  applicable while preserving unusual existing values and custom authoring.
  Clarify the separate **Activate** and **Activations** editors before changing
  their presentation; they use different storage paths and must not lose data.
  Keep description and common equipment properties easy to reach.
  Sources: `forms/item.json`, `forms/partials/item-type.json`, and
  `../dnd5e-source/forms/item.json`.
  Implemented on 2026-10-05: category/level/rarity/traits/subcategory share the
  opening group; price, usage, and bulk remain direct. A root-context
  **Additional details** summary/editor collects ammunition, onset, and
  crafting requirements, available for every category even when empty.
  Armor/shield/weapon/gear properties remain direct and populated exceptional
  properties retain an editing route after category changes. **Primary
  activation** and **Additional activations** clarify the separate single
  activation and named-entry list without changing their storage or schemas.
  Item types are labeled **Variants** in the editor. Top-level sections decrease
  from 12 to 10, with typical non-category rows decreasing from 15 to 13.
  All 38 bound controls preserve paths, input types, defaults, and units;
  English/French labels, summaries, and the existing editability suite were
  updated. Focused and canonical checks pass. The user approved the layout on
  2026-10-05, reporting no issues and much better organization; individual
  save/reopen checks were not separately reported. The user chose creatures
  next, ahead of the shared ability editor.
- [x] **3. Give abilities a clearer writing flow — source complete; user tests pass.**
  The 5e monster feature editor centers on Name, Usage, and Description. Ours
  always gives Description, Trigger, Effect, and Reference separate sections.
  Keep the PF2E distinctions, but compact optional material, put an applicable
  trigger in a clear reading order, and retain separate editing of description,
  trigger, effect, traits, action cost, and reference. Improve labels without
  conflating passive abilities, actions, and reactions.
  Sources: `forms/partials/ability.json`, `views/partials/ability.md`, and
  `../dnd5e-source/forms/partials/monster-feature.json`.
  Implemented on 2026-10-05: Name, **Action cost**, and Traits share the opening
  group. **Rules text** follows Trigger (optional) → Description → Effect →
  Linked action (optional), with short localized writing prompts distinguishing
  activation conditions, context/passive rules, and the resulting effect.
  Six sections become two; all seven original controls remain directly
  accessible with identical paths, types, attribute types, defaults, units,
  and visibility. Trigger and Effect remain available for every action cost,
  including passive/free-action abilities. Creature interaction/defensive/
  offensive entries, item activations, hazards, and vehicles share this partial.
  No additional editor level, data conversion, or rendering change was added;
  the existing trigger-order/paragraph flags and stat-block references remain
  intact. English/French labels are included. The existing editability suite
  covers all seven bindings and source-text preservation and passes, as does
  the canonical source check. The user approved the result and reported a
  native pass on 2026-10-05; that confirmation is recorded in `STATUS.md`.
- [x] **4. Creature layout and terminology — source complete; user tests pass.**
  Our creature form has 18 top-level sections versus 11 in the 5e monster form.
  Level alone, Base Traits, and Other Traits fragment the opening. Organize
  related edits around **Identity**, **Statistics**, **Defenses**, and
  **Actions & Magic**; choose groups or tabs according to the actual editing
  flow. Keep ordinary statistics direct and exceptional notes accessible.
  Shorten long ability-category labels while preserving their meaning, and
  fix the existing **Ractive** typo.
  Sources: `forms/creature.json`, `lang/en.json`, and
  `../dnd5e-source/forms/monster.json`.
  Selected by the user on 2026-10-05, with extra care to preserve previous
  optimization/refresh work. Implemented four native tabs following the official
  5e character form's tab mechanism: **Identity** (level/rarity/size/traits,
  Recall Knowledge, inventory, interaction abilities), **Statistics**
  (perception, senses, Skills/Lore, Speed, attribute modifiers, languages/notes),
  **Defenses** (AC/HP/hardness and notes, saving throws/notes, immunities,
  weaknesses/resistances, automatic/reactive abilities), and **Actions & Magic**
  (attacks, spellcasting, rituals, offensive/proactive abilities). Sections
  decrease from 18 to 15, with at most four sections per tab. AC/HP notes have
  explicit labels; ability headings are shorter and the Ractive typo is fixed.
  All existing subforms/list entries and their navigation remain intact.
  A before/after audit verified all 118 resolved control bindings through
  nested partials, including their input types, defaults, units, visibility,
  and list metadata. Shared ability, attack/damage, spellcasting, and ritual
  partials were not changed. The maintained editability suite now traverses
  tabs and guards the complete inline path set and direct ordinary stats.
  Focused editability/spellcasting checks and the canonical source check pass.
  The user approved the layout and reported all tests passing on 2026-10-05.
  Preserve that native pass when working on summaries. Shared abilities remain
  a separate unchecked step.
- [x] **5. Improve summaries before adding more nested screens — source complete; user tests pass.**
  Creature spell edits traverse casting entry, spell group, and individual
  spell; attack damage components also have their own editors. Improve parent
  summaries with attack modifiers, damage formulas/types, spell ranks, and
  relevant usage details. Evaluate direct weakness/resistance lists in the
  Defenses area to remove an intermediary screen. Preserve structured damage
  components, casting groups, slots, uses, at-will/constant notes, and links;
  do not replace them with free text to reduce clicks.
  Sources: `forms/partials/attack.json`, `forms/partials/damage-part.json`,
  `forms/partials/spellcasting*.json`, `forms/partials/defense-entry.json`, and
  `forms/creature.json`.
  Implemented on 2026-10-05: attack rows preview melee/ranged type, action cost,
  signed modifier, structured damage formulas/types/connectors, and effect
  names, retaining legacy printed-damage and formula fallbacks. Damage rows
  explicitly preview the formula and type/effect. Casting rows preview DC,
  signed spell attack, focus points, and original rank-group labels; ritual
  rows retain DC and original group labels. Spell/ritual group previews add
  at-will and usage/constant notes to names. Entry previews localize rank and
  at-will labels, preserve rank/modifier zero, and omit missing rank labels.
  Character attack/casting rows reuse the same previews without changing
  character navigation. Cleared casting values omit their labels while zero
  values remain visible. All existing control paths, input types, defaults,
  units, visibility, list mappings/pickers, and routes are unchanged in a
  before/after comparison of nine affected/referenced form trees. No additional
  screens or content/migration changes were introduced. Reviewed direct
  weakness/resistance lists and retained their native-confirmed wrappers in
  this summary step; removing that screen remains a later candidate.
  Focused editability/spellcasting and canonical source checks pass. Following
  the numeric-input repair below, the user approved the latest package and
  reported all tests passing on 2026-10-05; the native pass is saved in `STATUS.md`.
  Native follow-up on 2026-10-05: the casting preview displays DC/attack and
  ranks correctly, and the user confirms rank groups load. Spell Attack/DC
  inputs nevertheless display None for numeric Astradaemon data. The inherited
  casting partial used text controls for those values before today's redesign;
  a separate repair changes only those two input types to `number`, with the
  original paths and groups intact. The user confirms the repair's native
  tests pass on 2026-10-05; the earlier creature layout pass is preserved.
- [x] **6. Character navigation — source complete; blank-state layout approved.**
  The 5e character editor has Main, Abilities & Skills, Inventory, and Spells
  tabs; ours has 12 sections in one continuous form. Use task-based tabs to
  make returning to statistics, inventory, and magic easier.
  Sources: `forms/character.json` and
  `../dnd5e-source/forms/character.json`.
  Implemented on 2026-10-05 using the same native tab containers and icons:
  **Main** holds identity, traits, HP, core statistics, movement, and resources;
  **Abilities & Skills** holds attribute modifiers, saves, skills, and attacks;
  **Inventory** holds equipment; **Spells** holds spellcasting entries. The
  original 12 sections are retained across tabs (6/4/1/1), with no added
  nested screen. All 63 resolved bound controls retain identical paths and
  metadata in a before/after audit, including root-context movement and
  row-context attack/casting editors. The inventory remains its existing
  editable text field. English/French tab labels are included. The maintained
  editability regression and canonical source check pass. On 2026-10-05, the
  user approved the overall layout of a blank character form; no populated
  character is available yet. Populated editing and save/reopen checks remain
  in `STATUS.md`.

Library selection for character ancestry, class, and equipment is a later
candidate. The 5e editor can select library entries where ours uses text; this
needs a separate data/compatibility design rather than a layout-only change.

**Completion and verification**

For each step, verify existing records and new/custom records preserve their
editable values, references, and behavior. Reuse the closest maintained suite
(including `tools/test_creature_editability.py`,
`tools/test_spell_area_templates.py`, and `tools/test_creature_spellcasting.py`
where relevant); add coverage only for behavior the suite does not cover.
Run focused checks while iterating and `.venv/bin/python tools/eplus_dev.py
check --json` once when the implementation is complete. Record source/check
completion separately from native-app verification; keep any pending app
checks in `STATUS.md`. Update this checklist as work is completed. Commit each
finished local step; do not bump versions, push, tag, or publish until requested.

## Additional source-backed possibilities

These are proven capabilities or useful authoring options, but are not yet
approved as the next implementation task.

### Dice links inside pages and records

Module Packer supports links such as `[Roll](/roll/1d20)`. These can turn
formulae in rules, tools, or roll-table results into native Encounter+ rolls.
Use them selectively where the formula is unambiguous; do not turn every number
in prose into a roll.

### Optional modules containing maps and encounters

Module Packer can package maps, encounters, pages, and related assets. Future
adventures or book-specific play material can therefore be distributed as
optional modules instead of bloating the core PF2E system.

### Automatically generated roll tables from authored modules

Module Packer's `create-roll-tables` option can convert properly authored dice-
range tables into Encounter+ roll tables. This could be useful for future
optional content modules after the native PF2E prototype is validated.

### Shop and equipment browsers

Module Packer includes a shop-table format with category and subcategory rows.
A compact, filterable equipment/shop reference with prices is technically
possible. The default filter must follow the actual market rules rather than
showing every priced item: common, priced items at or below the settlement
level are the normal stock; the settlement's highest-level stock is limited;
items above that level require special ordering or GM placement; and uncommon
items only become normal stock when the buyer or settlement meets their Access
entry. Rare and unique items must not appear as routine shop inventory. The
item data supports level, rarity, category, Price, source, and page where known;
explicit Access text can be extracted from item descriptions when present.

### Load actions for supported entity types

The official 5e entity definitions demonstrate native load actions for spells,
vehicles, characters, monsters, and NPCs. PF2E spell loading now uses this for
area templates and token status effects. Other load actions should only be
added when they produce a clear Encounter+ map or encounter behavior rather
than merely duplicating a Library record.

### HTML/JavaScript GM tools

The Operations Center and Encounter XP Planner prove that compact interactive
tools can live inside the system. Additional selectors or calculators are
possible, but only when they remain usable in Encounter+'s narrow bookmark
panel and link back to the complete sourced rule.

## Completed source-backed improvements

- Native PF2E entity forms and views, including book-style hazard and vehicle
  stat blocks.
- Sources, pages, GP values, errata corrections, and internal links for the
  data families already audited.
- Twenty-four sourced native reference tables and compact Operations Center
  selectors.
- Encounter XP Planner and bookmarkable Operations Center.
- Safe structured spell-area templates, including radius mapping for
  emanations where Encounter+ cannot express a distinct emanation type.
- Native spell loading onto selected tokens, with printed durations mapped to
  timers/turn endings or manual reminders, without expanding the general
  status-effect menu into a spell catalog.
- Spell-editor compatibility with the rebuilt native forms, including valid
  nested numeric fields and recursive form-schema checks.
- Compact entity views that retain their theme and resize text to fit the host
  Library/search panel.
- Packaging, validation, release inspection, update manifests, and migrations.

## Deliberately closed or deferred ideas

- **Per-token initiative-skill overrides:** the status-effect experiment was
  unreliable and was reverted. Library creatures retain Perception by default.
- **Rule automation:** native spell-effect timers and turn endings are now
  supported. Automatic modifiers, Sustain, and rule-dependent early endings
  remain the GM's responsibility.
- **Timers for placed map areas:** deferred because native `AreaEffect`
  records expose no duration or expiry fields. A placed area such as Frozen
  Fog cannot inherit automatic expiry through system spell data. The user
  requested aborting this change unless the host supports it; no workaround
  was added. Reconsider when Encounter+ provides native area-duration support.
- **Virtual 3D dice in the web client:** rejected because recreating the app's
  renderer and server behavior is too much maintenance for the benefit.
- **Persistent/saved player area templates:** unnecessary for previews and
  unsafe to publish to the shared map without an explicit GM permission.
- **Player-published area templates:** reconsider only if Encounter+ exposes a
  host-controlled permission for it.
- **Manual templates for ambiguous spells:** leave these spells unchanged.
  Quick Load is only useful when the spatial result can be generated safely.
