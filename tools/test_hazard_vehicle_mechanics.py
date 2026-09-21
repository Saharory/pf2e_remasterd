"""Regression checks for published hazard and vehicle mechanics."""

from __future__ import annotations

import copy
import json
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))

from hazard_vehicle_mechanics import STRIKES, supplement


class HazardVehicleMechanicsTests(unittest.TestCase):
    def test_strike_fixture_is_present_in_published_hazards(self) -> None:
        hazards = {
            record["slug"]: record
            for path in (ROOT / "compendium/packs").glob("*/hazards.json")
            for record in json.loads(path.read_text())
        }
        self.assertEqual(set(STRIKES), set(STRIKES) & hazards.keys())
        for slug, expected in STRIKES.items():
            record = hazards[slug]
            self.assertEqual(record["data"]["attacks"], expected)
            self.assertTrue(record["sources"])

    def test_supplement_does_not_replace_custom_strikes(self) -> None:
        record = {"slug": "spear-launcher-gm-core", "data": {"attacks": [{"name": "Custom"}]}}
        supplement(record, "Hazard")
        self.assertEqual(record["data"]["attacks"], [{"name": "Custom"}])

    def test_vehicle_prices_show_gp_without_inventing_zero_price(self) -> None:
        for price, expected in ((6000, "6,000 gp"), ("480 gp", "480 gp"), (0, "")):
            record = {"data": {"price": price}}
            supplement(record, "Vehicle")
            self.assertEqual(record["data"].get("price"), expected)

    def test_all_published_vehicle_prices_match_display(self) -> None:
        for path in (ROOT / "compendium/packs").glob("*/vehicles.json"):
            for record in json.loads(path.read_text()):
                rebuilt = copy.deepcopy(record)
                supplement(rebuilt, "Vehicle")
                self.assertEqual(rebuilt["data"], record["data"])

    def test_views_expose_mechanics_and_editors(self) -> None:
        for kind, fields in (
            ("hazard", ("data.stealth", "data.disable", "data.attacks", "data.abilities", "data.routine", "data.reset")),
            ("vehicle", ("data.price", "data.space.long", "data.pilotingCheck", "data.collisionDamage", "data.abilities")),
        ):
            view = json.loads((ROOT / f"views/{kind}.json").read_text())
            form = json.loads((ROOT / f"forms/{kind}.json").read_text())
            self.assertIn(f'{kind}-stats.md', json.dumps(view))
            combined = (ROOT / f"views/partials/{kind}-stats.md").read_text() + json.dumps(form)
            for field in fields:
                self.assertIn(field, combined)

    def test_new_partials_use_balanced_supported_control_tags(self) -> None:
        for kind in ("hazard", "vehicle"):
            content = (ROOT / f"views/partials/{kind}-stats.md").read_text()
            stack = []
            for tag in re.findall(r"{%\s*(\w+)[^%]*%}", content):
                if tag in {"if", "for"}:
                    stack.append(tag)
                elif tag in {"endif", "endfor"}:
                    self.assertTrue(stack, f"{kind}: stray {tag}")
                    self.assertEqual(stack.pop(), tag.removeprefix("end"))
                else:
                    self.assertIn(tag, {"else", "include"}, f"{kind}: unsupported {tag}")
            self.assertFalse(stack, f"{kind}: unclosed tags {stack}")


if __name__ == "__main__":
    unittest.main()
