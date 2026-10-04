# PF2E Remaster and Web Client Roadmap

Last reviewed: 2026-10-04

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
