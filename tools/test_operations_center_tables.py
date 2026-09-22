#!/usr/bin/env python3
"""Compact bookmark-panel reference tables stay linked to the ORC source."""

import json
import re
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from build_operations_center import REPO, pages, reference_picker, reference_tables, validate, groups


class OperationsCenterTableTests(unittest.TestCase):
    def test_picker_is_single_row_and_source_backed(self) -> None:
        markup = reference_picker("DC", ["DCs by Level"], "20")
        payload = json.loads(re.search(r'<script type="application/json" data-ops-payload>(.*?)</script>', markup).group(1))
        source = reference_tables()["DCs by Level"]
        self.assertEqual(payload[0]["rows"], source["rows"])
        self.assertIn('<span>40</span>', markup)
        self.assertIn("/table/dcs-by-level-gm-core", markup)
        self.assertNotIn("<table", markup)

    def test_all_creature_levels_and_stats_fit_one_picker(self) -> None:
        names = [name for name in reference_tables() if name.startswith("Creature Building — ")]
        markup = reference_picker("Benchmarks", names)
        self.assertEqual(markup.count('data-ops-reference>'), 1)
        self.assertIn('data-ops-stat', markup)
        self.assertIn('value="–1"', markup)
        self.assertIn('value="24"', markup)

    def test_generated_pages_keep_valid_table_routes(self) -> None:
        generated = [page.record() for page in pages()]
        validate(generated, groups())
        saved = json.loads((REPO / "pages.json").read_text())
        self.assertEqual(saved, generated)
        creature = next(page for page in saved if page["slug"] == "pf2e-ops-creature-benchmarks")
        self.assertIn("data-ops-reference", creature["content"])
        self.assertIn("/table/creature-building-attribute-modifiers-gm-core", creature["content"])


if __name__ == "__main__":
    unittest.main()
