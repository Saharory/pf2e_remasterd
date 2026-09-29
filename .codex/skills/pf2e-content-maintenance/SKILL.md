---
name: pf2e-content-maintenance
description: Maintain generated PF2E records when importing, auditing, repairing, or linking licensed compendium content.
---

Trace a record to `../structured-modules` and its builder before editing. Fix
the converter for repeated defects; use a supplement only for true source
exceptions.

Use current licensed rules and errata as the mechanical authority. AoN is useful
for links and presentation; Foundry data is useful for structured fields and
relationships. Neither proves that prose is distributable. Prefer text or
structured data; inspect a cropped image only for unresolved presentation.

Preserve reliable source data, internal links, Remaster terminology, ORC/OGL
markers, and editability for every displayed mechanic except map-only actions.

Rebuild affected packs and extend the owning regression suite. Use focused
checks while iterating, then run `python3 tools/eplus_dev.py check --json` once.
