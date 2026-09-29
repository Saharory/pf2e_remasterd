---
name: encounterplus-development
description: Develop Encounter+ entities, forms, views, packages, or GM tools when changing system structure or native integration.
---

Consult `ROADMAP.md` only for product decisions and `STATUS.md` only for the
latest handoff.

Establish the supported Encounter+ mechanism before inventing a parallel one.
Inspect the current official repositories already available beside this project
when schemas, package formats, migrations, or native behavior are uncertain.
Distinguish app-owned behavior from system/package behavior; report when the
public interface cannot express a feature safely.

Keep compact panels useful at Encounter+'s narrow embedded width. Prefer
structured editable fields and internal routes over duplicated prose or custom
JavaScript. Use map loading only when placement has a clear native form.

Extend the closest regression, run focused checks while iterating, and run the
canonical check once at completion. Record native-app testing separately in
`STATUS.md`; a package build is not proof of app behavior.
