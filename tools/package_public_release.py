#!/usr/bin/env python3
"""Create installable Encounter+ archives from the reviewed public tree."""

from __future__ import annotations

import argparse
import zipfile
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=REPO / "dist")
    return parser.parse_args()


def archive(directory: Path, target: Path, excluded_roots: set[str] | None = None) -> None:
    excluded_roots = excluded_roots or set()
    with zipfile.ZipFile(target, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as bundle:
        for path in sorted(directory.rglob("*")):
            relative = path.relative_to(directory)
            if not path.is_file() or any(part.startswith(".") for part in relative.parts):
                continue
            if relative.parts and relative.parts[0] in excluded_roots:
                continue
            bundle.write(path, relative)


def main() -> int:
    args = parse_args()
    args.output.mkdir(parents=True, exist_ok=True)

    archive(
        REPO,
        args.output / "pf2e-remaster.system",
        excluded_roots={"compendium", "dist", "tools"},
    )

    pack_count = 0
    for pack in sorted((REPO / "compendium" / "packs").iterdir()):
        if not pack.is_dir() or not (pack / "module.json").is_file():
            continue
        archive(pack, args.output / f"{pack.name}.module")
        pack_count += 1

    print(f"Packaged one system and {pack_count} ORC modules in {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
