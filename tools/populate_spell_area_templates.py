#!/usr/bin/env python3
"""Populate supported area-template fields in the published spell packs."""

from __future__ import annotations

import json
from pathlib import Path

from spell_area_templates import configure_spell_area_template


REPO = Path(__file__).resolve().parents[1]


def main() -> None:
    area_spells = 0
    configured = 0
    skipped = 0
    files = 0

    roots = (REPO / "compendium" / "packs", REPO / "compendium" / "ogl-packs")
    for root in roots:
        for path in sorted(root.glob("*/spells.json")):
            records = json.loads(path.read_text(encoding="utf-8"))
            changed = False
            for record in records:
                data = record.get("data") or {}
                before = (data.get("areaEffectShape"), data.get("areaEffectSize"))
                if str(data.get("area") or "").strip():
                    area_spells += 1
                    if configure_spell_area_template(record):
                        configured += 1
                    else:
                        skipped += 1
                else:
                    configure_spell_area_template(record)
                after = (data.get("areaEffectShape"), data.get("areaEffectSize"))
                changed = changed or before != after

            if changed:
                path.write_text(
                    json.dumps(records, ensure_ascii=False, indent=2) + "\n",
                    encoding="utf-8",
                )
                files += 1

    print(
        f"spell areas: {configured} configured, {skipped} intentionally skipped "
        f"from {area_spells} area spells across {files} files"
    )


if __name__ == "__main__":
    main()
