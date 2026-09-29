---
name: encounterplus-development
description: Design or implement Encounter+ system entities, forms, views, packages, native rolls, load actions, or GM tools.
---

Use `ROADMAP.md` when the task needs an existing product decision and
`STATUS.md` when it needs the latest handoff. Do not restate those files here.

Establish the supported Encounter+ mechanism before inventing a parallel one.
Inspect the current official repositories already available beside this project
when entity schemas, package formats, forms, views, migrations, or native app
behavior are uncertain. Distinguish app-owned behavior from system/package
behavior and report when the public interface cannot express a requested
feature safely.

Keep compact panels useful at Encounter+'s narrow embedded width. Prefer
structured editable fields and internal routes over duplicated prose or custom
JavaScript. Use map load behavior only when placement has an unambiguous native
representation.

Extend the relevant existing test domain and finish with the repository's
canonical check command. Native Encounter+ testing remains a separate result:
record it as pending or verified in `STATUS.md` rather than treating a package
build as proof of app behavior.
