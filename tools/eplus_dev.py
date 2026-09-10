#!/usr/bin/env python3
"""Fast, safe development commands for the Encounter+ PF2E system.

This tool intentionally never edits Encounter+'s database and never deletes
installed content. Definition files can be checksum-synced to the installed
system folder, after which the app's supported Reload System action picks them
up. Content modules still go through Encounter+'s importer.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path
from typing import Any, Iterable


REPO = Path(__file__).resolve().parents[1]
DEFAULT_TARGET = (
    Path.home()
    / "Library/Containers/sk.qbit.tracker/Data/Documents/systems/pf2e-remaster"
)
SYSTEM_ID = "pf2e-remaster"
SEMVER = re.compile(r"^\d+\.\d+\.\d+(?:[-+][0-9A-Za-z.-]+)?$")
SYSTEM_FILES = {
    "system.json",
    "manifest.json",
    "config.json",
    "entities.json",
    "types.json",
    "collections.json",
    "filters.json",
    "COMMUNITY-USE-NOTICE.md",
}
SYSTEM_DIRS = {
    "fonts",
    "forms",
    "icons",
    "images",
    "lang",
    "scripts",
    "styles",
    "themes",
    "views",
}
COLLECTION_TITLES = {
    "actions": "Actions",
    "afflictions": "Afflictions",
    "ancestries": "Ancestries",
    "archetypes": "Archetypes",
    "backgrounds": "Backgrounds",
    "characters": "Characters",
    "classes": "Classes",
    "conditions": "Conditions & Effects",
    "creatures": "Creatures",
    "deities": "Deities",
    "domains": "Domains",
    "feats": "Feats",
    "hazards": "Hazards",
    "heritages": "Heritages",
    "items": "Items",
    "languages": "Languages",
    "rituals": "Rituals",
    "rules": "Rules",
    "spells": "Spells",
    "traits": "Traits",
    "vehicles": "Vehicles",
}
LABEL_TO_COLLECTION = {
    "action": "actions",
    "affliction": "afflictions",
    "ancestry": "ancestries",
    "archetype": "archetypes",
    "background": "backgrounds",
    "character": "characters",
    "hero": "characters",
    "class": "classes",
    "condition": "conditions",
    "status-effect": "conditions",
    "creature": "creatures",
    "deity": "deities",
    "domain": "domains",
    "feat": "feats",
    "hazard": "hazards",
    "heritage": "heritages",
    "item": "items",
    "language": "languages",
    "ritual": "rituals",
    "rule": "rules",
    "spell": "spells",
    "trait": "traits",
    "vehicle": "vehicles",
}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def load_json5(path: Path) -> Any:
    try:
        import json5  # type: ignore
    except ModuleNotFoundError as exc:
        raise RuntimeError(
            "Missing development dependency 'json5'. Run: "
            "python3 -m pip install -r requirements-dev.txt"
        ) from exc
    return json5.loads(path.read_text(encoding="utf-8"), allow_duplicate_keys=False)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def definition_files() -> list[Path]:
    files = [REPO / name for name in sorted(SYSTEM_FILES) if name.endswith(".json")]
    for directory in sorted(SYSTEM_DIRS):
        root = REPO / directory
        if root.is_dir():
            files.extend(sorted(root.rglob("*.json")))
    return files


def sync_files() -> list[Path]:
    files = [REPO / name for name in sorted(SYSTEM_FILES) if (REPO / name).is_file()]
    for directory in sorted(SYSTEM_DIRS):
        root = REPO / directory
        if not root.is_dir():
            continue
        files.extend(
            path
            for path in sorted(root.rglob("*"))
            if path.is_file()
            and not any(part.startswith(".") for part in path.relative_to(REPO).parts)
            and "__pycache__" not in path.parts
        )
    return files


def run_validator(script: str) -> tuple[bool, str]:
    result = subprocess.run(
        [sys.executable, str(REPO / "tools" / script)],
        cwd=REPO,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    lines = [line.strip() for line in result.stdout.splitlines() if line.strip()]
    return result.returncode == 0, lines[-1] if lines else script


def validate_project() -> dict[str, Any]:
    errors: list[str] = []
    parsed = 0
    for path in definition_files():
        try:
            load_json5(path)
            parsed += 1
        except Exception as exc:  # decoder messages are the useful result here
            errors.append(f"{path.relative_to(REPO)}: {exc}")

    try:
        system = load_json5(REPO / "system.json")
        manifest = load_json(REPO / "manifest.json")
        for field in ("id", "name", "version"):
            if not system.get(field):
                errors.append(f"system.json: missing {field}")
        for field in ("id", "name", "type", "version", "download"):
            if not manifest.get(field):
                errors.append(f"manifest.json: missing {field}")
        if system.get("id") != SYSTEM_ID or manifest.get("id") != SYSTEM_ID:
            errors.append("system and package ids must both be pf2e-remaster")
        if manifest.get("type") != "system":
            errors.append("manifest.json: type must be system")
        if system.get("version") != manifest.get("version"):
            errors.append("system.json and manifest.json versions differ")
        if not SEMVER.match(str(system.get("version") or "")):
            errors.append("system.json: version is not semantic versioning")
        if not str(system.get("package") or "").endswith("/manifest.json"):
            errors.append("system.json: package must point at the latest manifest")
        if not str(manifest.get("download") or "").endswith("/pf2e-remaster.system"):
            errors.append("manifest.json: download must point at pf2e-remaster.system")

        entities = load_json5(REPO / "entities.json")
        names: set[str] = set()
        labels: set[str] = set()
        collections: set[str] = set()
        for index, entity in enumerate(entities):
            name = str(entity.get("name") or "")
            label = str(entity.get("label") or "")
            collection = str((entity.get("collection") or {}).get("label") or "")
            if not name or not label or not collection:
                errors.append(f"entities.json[{index}]: missing name, label, or collection")
            if name in names or label in labels or collection in collections:
                errors.append(f"entities.json[{index}]: duplicate entity identifier")
            names.add(name)
            labels.add(label)
            collections.add(collection)
    except Exception as exc:
        errors.append(f"metadata validation: {exc}")

    ogl_root = REPO / "compendium" / "ogl-packs" / "rage-of-elements"
    try:
        module = load_json(ogl_root / "module.json")
        ogl_manifest = load_json(ogl_root / "manifest.json")
        if module.get("id") != ogl_manifest.get("id"):
            errors.append("Rage of Elements module and manifest ids differ")
        if module.get("version") != ogl_manifest.get("version"):
            errors.append("Rage of Elements module and manifest versions differ")
        if ogl_manifest.get("type") != "module":
            errors.append("Rage of Elements manifest type must be module")
        if ogl_manifest.get("system") != SYSTEM_ID:
            errors.append("Rage of Elements manifest targets the wrong system")
        if not str(module.get("package") or "").endswith(
            "/rage-of-elements-ogl-manifest.json"
        ):
            errors.append("Rage of Elements module package URL is missing")
    except Exception as exc:
        errors.append(f"Rage of Elements metadata validation: {exc}")

    validators: dict[str, str] = {}
    for script in (
        "validate_public_orc_compendium.py",
        "validate_public_ogl_compendium.py",
    ):
        ok, message = run_validator(script)
        validators[script] = message
        if not ok:
            errors.append(f"{script}: {message}")

    return {
        "ok": not errors,
        "definitionFiles": parsed,
        "validators": validators,
        "errors": errors,
    }


def git_changes() -> list[str]:
    commands = (
        ["git", "diff", "--name-only", "HEAD"],
        ["git", "ls-files", "--others", "--exclude-standard"],
    )
    paths: set[str] = set()
    for command in commands:
        result = subprocess.run(
            command,
            cwd=REPO,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        paths.update(line for line in result.stdout.splitlines() if line)
    return sorted(paths)


def impacted_collections(paths: Iterable[str]) -> list[str]:
    impacted: set[str] = set()
    all_collections = False
    for value in paths:
        path = Path(value)
        if path.name in {"manifest.json", "system.json"} and "compendium" not in path.parts:
            impacted.add("System package details")
            continue
        if path.parts and path.parts[0] in {"styles", "themes", "scripts"}:
            all_collections = True
            continue
        if path.name in {
            "config.json",
            "entities.json",
            "types.json",
            "collections.json",
            "filters.json",
        }:
            all_collections = True
            continue
        if path.parts and path.parts[0] in {"forms", "views"}:
            if "partials" in path.parts:
                all_collections = True
                continue
            label = path.stem.removesuffix("-compact")
            collection = LABEL_TO_COLLECTION.get(label)
            if collection:
                impacted.add(collection)
            continue
        if "compendium" in path.parts and path.suffix == ".json":
            if path.stem in COLLECTION_TITLES:
                impacted.add(path.stem)
    if all_collections:
        return ["All compendium views"]
    return [COLLECTION_TITLES.get(name, name) for name in sorted(impacted)]


def sync_status(target: Path) -> dict[str, Any]:
    changed: list[str] = []
    missing: list[str] = []
    same = 0
    for source in sync_files():
        relative = source.relative_to(REPO)
        destination = target / relative
        if not destination.is_file():
            missing.append(relative.as_posix())
        elif sha256(source) != sha256(destination):
            changed.append(relative.as_posix())
        else:
            same += 1
    candidates = sorted(changed + missing)
    return {
        "target": str(target),
        "changed": sorted(changed),
        "missing": sorted(missing),
        "unchanged": same,
        "uiTargets": impacted_collections(candidates),
    }


def verify_target(target: Path) -> None:
    if not target.is_dir():
        raise RuntimeError(f"installed system folder not found: {target}")
    installed = load_json5(target / "system.json")
    if installed.get("id") != SYSTEM_ID:
        raise RuntimeError(f"refusing to sync into a different system: {target}")


def sync_system(target: Path, apply: bool) -> dict[str, Any]:
    check = validate_project()
    if not check["ok"]:
        return {"ok": False, "applied": False, "errors": check["errors"]}
    verify_target(target)
    status = sync_status(target)
    copied: list[str] = []
    if apply:
        for relative in status["changed"] + status["missing"]:
            source = REPO / relative
            destination = target / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, destination)
            copied.append(relative)
    return {
        "ok": True,
        "applied": apply,
        "copied": sorted(copied),
        "pending": [] if apply else sorted(status["changed"] + status["missing"]),
        "unchanged": status["unchanged"],
        "uiTargets": status["uiTargets"],
        "note": "No files are ever deleted by sync-system.",
    }


def clean_zip_names(names: Iterable[str]) -> list[str]:
    return sorted(
        name
        for name in names
        if "__MACOSX" in Path(name).parts
        or any(part.startswith("._") for part in Path(name).parts)
        or Path(name).name == ".DS_Store"
    )


def inspect_release(dist: Path) -> dict[str, Any]:
    errors: list[str] = []
    system_path = dist / "pf2e-remaster.system"
    ogl_path = dist / "rage-of-elements-ogl.module"
    required = {
        system_path,
        ogl_path,
        dist / "manifest.json",
        dist / "rage-of-elements-ogl-manifest.json",
        dist / "release-summary.json",
        dist / "SHA256SUMS.txt",
    }
    for path in sorted(required):
        if not path.is_file():
            errors.append(f"missing release file: {path.name}")

    orc_records = 0
    orc_ids: set[str] = set()
    collection_counts: dict[str, int] = {}
    if system_path.is_file():
        with zipfile.ZipFile(system_path) as bundle:
            names = set(bundle.namelist())
            junk = clean_zip_names(names)
            if junk:
                errors.append(f"system archive contains macOS junk: {junk[:3]}")
            for required_name in (
                "system.json",
                "manifest.json",
                "ORC-NOTICE.md",
                "COMMUNITY-USE-NOTICE.md",
                "notices/ORC-SOURCES.json",
            ):
                if required_name not in names:
                    errors.append(f"system archive missing {required_name}")
            if "module.json" in names or "OGL-1.0a.txt" in names:
                errors.append("system archive crossed the ORC/OGL package boundary")

            for name in sorted(names):
                if name not in {f"{label}.json" for label in COLLECTION_TITLES}:
                    continue
                records = json.loads(bundle.read(name))
                collection_counts[name] = len(records)
                orc_records += len(records)
                for record in records:
                    record_id = str(record.get("id") or "")
                    if not record_id or record_id in orc_ids:
                        errors.append(f"missing or duplicate ORC entity id in {name}")
                        break
                    orc_ids.add(record_id)
                    if record.get("system") != SYSTEM_ID:
                        errors.append(f"wrong entity system in {name}")
                        break
                    if (record.get("attributes") or {}).get("license") != "ORC-1.0a":
                        errors.append(f"non-ORC entity found in {name}")
                        break
                    if not str((record.get("data") or {}).get("sourceName") or "").strip():
                        errors.append(f"ORC entity missing packaged source name in {name}")
                        break

    ogl_records = 0
    if ogl_path.is_file():
        with zipfile.ZipFile(ogl_path) as bundle:
            names = set(bundle.namelist())
            junk = clean_zip_names(names)
            if junk:
                errors.append(f"OGL module contains macOS junk: {junk[:3]}")
            for required_name in (
                "module.json",
                "manifest.json",
                "OGL-1.0a.txt",
                "COMMUNITY-USE-NOTICE.md",
            ):
                if required_name not in names:
                    errors.append(f"OGL module missing {required_name}")
            if "ORC-NOTICE.md" in names or "system.json" in names:
                errors.append("OGL module crossed the system/ORC package boundary")
            for name in sorted(names):
                if name not in {f"{label}.json" for label in COLLECTION_TITLES}:
                    continue
                records = json.loads(bundle.read(name))
                ogl_records += len(records)
                for record in records:
                    if (record.get("attributes") or {}).get("license") != "OGL-1.0a":
                        errors.append(f"non-OGL entity found in OGL {name}")
                        break

    expected_orc = sum(
        sum(kinds.values()) for kinds in load_json(REPO / "compendium" / "summary.json").values()
    )
    expected_ogl = sum(
        sum(kinds.values())
        for kinds in load_json(REPO / "compendium" / "ogl-summary.json").values()
    )
    if orc_records != expected_orc:
        errors.append(f"ORC record count {orc_records} != expected {expected_orc}")
    if ogl_records != expected_ogl:
        errors.append(f"OGL record count {ogl_records} != expected {expected_ogl}")

    return {
        "ok": not errors,
        "installablePackages": 2,
        "orcRecords": orc_records,
        "oglRecords": ogl_records,
        "collectionCounts": collection_counts,
        "systemBytes": system_path.stat().st_size if system_path.is_file() else 0,
        "oglBytes": ogl_path.stat().st_size if ogl_path.is_file() else 0,
        "errors": errors,
    }


def emit(result: dict[str, Any], compact: bool) -> None:
    if compact:
        print(json.dumps(result, separators=(",", ":"), ensure_ascii=False))
    else:
        print(json.dumps(result, indent=2, ensure_ascii=False))


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(description=__doc__)
    commands = root.add_subparsers(dest="command", required=True)

    check = commands.add_parser("check", help="run local syntax, metadata, and license checks")
    check.add_argument("--json", action="store_true", help="emit one compact JSON line")

    status = commands.add_parser("status", help="show changed files and targeted UI checks")
    status.add_argument("--target", type=Path, default=DEFAULT_TARGET)
    status.add_argument("--json", action="store_true", help="emit one compact JSON line")

    sync = commands.add_parser("sync-system", help="checksum-sync system definition files")
    sync.add_argument("--target", type=Path, default=DEFAULT_TARGET)
    sync.add_argument("--apply", action="store_true", help="copy files; default is dry-run")
    sync.add_argument("--json", action="store_true", help="emit one compact JSON line")

    inspect = commands.add_parser("inspect-release", help="inspect generated release archives")
    inspect.add_argument("--dist", type=Path, default=REPO / "dist")
    inspect.add_argument("--json", action="store_true", help="emit one compact JSON line")
    return root


def main() -> int:
    args = parser().parse_args()
    if args.command == "check":
        result = validate_project()
    elif args.command == "status":
        verify_target(args.target)
        changes = git_changes()
        result = {
            "ok": True,
            "gitChanges": changes,
            "gitUiTargets": impacted_collections(changes),
            "sync": sync_status(args.target),
        }
    elif args.command == "sync-system":
        result = sync_system(args.target, args.apply)
    else:
        result = inspect_release(args.dist)
    emit(result, args.json)
    return 0 if result.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
