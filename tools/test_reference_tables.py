#!/usr/bin/env python3
"""Regression checks for source-backed Encounter+ reference tables."""

import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from build_reference_tables import PACKS, build_tables, markdown_tables


class ReferenceTableTests(unittest.TestCase):
    def test_source_table_parser_preserves_links_and_dice(self) -> None:
        tables = markdown_tables(
            "| **Name** | **Result** |\n| --- | --- |\n"
            "| [Cover](/rule/cover-rules-2372) | 2d6 |"
        )
        self.assertEqual(tables, [
            (["Name", "Result"], [["[Cover](/rule/cover-rules-2372)", "2d6"]])
        ])

    def test_curated_tables_match_published_rules_and_sources(self) -> None:
        for source_id, expected_count in (("gm-core", 21), ("player-core", 3)):
            with self.subTest(source_id=source_id):
                path = PACKS / source_id
                rules = json.loads((path / "rules.json").read_text())
                saved = json.loads((path / "tables.json").read_text())
                self.assertEqual(saved, build_tables(rules, source_id))
                self.assertEqual(len(saved), expected_count)
                self.assertEqual(len({table["id"] for table in saved}), expected_count)
                self.assertTrue(all(table["sources"][0].get("page") for table in saved))
                self.assertTrue(all(table["attributes"]["license"] == "ORC-1.0a" for table in saved))

    def test_key_numbers_and_detection_links(self) -> None:
        gm = {table["name"]: table for table in json.loads((PACKS / "gm-core/tables.json").read_text())}
        player = {table["name"]: table for table in json.loads((PACKS / "player-core/tables.json").read_text())}
        self.assertIn(["20", "40"], gm["DCs by Level"]["rows"])
        self.assertEqual(gm["Simple DCs"]["sources"][0]["page"], 53)
        self.assertIn(["Extreme", "160", "40"], gm["Encounter XP Budget"]["rows"])
        self.assertIn(["Thin wood", "3", "12", "6", "Chair, club, sapling, wooden shield"],
                      gm["Material Hardness, HP, and BT"]["rows"])
        self.assertIn(["Standard", "+2 to AC, Reflex, Stealth", "Yes"], player["Cover"]["rows"])
        self.assertEqual(player["Detection and Targeting"]["rows"][1][2], "DC 11")
        self.assertIn("/rule/hidden-rules-2416", player["Detection and Targeting"]["rows"][1][0])


if __name__ == "__main__":
    unittest.main()
