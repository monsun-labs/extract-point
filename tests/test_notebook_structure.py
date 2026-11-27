"""Structural checks on the tutorial notebook (no cell execution)."""
from __future__ import annotations

import json
import unittest
from pathlib import Path

NB = Path(__file__).resolve().parents[1] / "notebooks" / "extract_point.ipynb"


class NotebookStructureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        nb = json.loads(NB.read_text(encoding="utf-8"))
        parts: list[str] = []
        for cell in nb["cells"]:
            src = cell.get("source", [])
            if isinstance(src, list):
                parts.extend(src)
            else:
                parts.append(src)
        cls.src = "".join(parts)
        cls.n_cells = len(nb["cells"])

    def test_bootstrap_and_utils(self) -> None:
        self.assertIn("monsun-labs/extract-point.git", self.src)
        self.assertIn("requirements-notebook", self.src)
        self.assertIn("lat_idx", self.src)
        self.assertIn("extract_utils", self.src)
        self.assertIn("add_wind_speed", self.src)

    def test_no_known_breakage(self) -> None:
        self.assertNotIn("latitude=42", self.src)
        self.assertNotIn("era5_natuna", self.src)
        self.assertNotIn("colab-link", self.src)
        self.assertNotIn("monsunlab/", self.src)
        self.assertNotIn("nusawave-labs", self.src)
        self.assertNotIn("Nusawave", self.src)

    def test_cell_count_reasonable(self) -> None:
        self.assertGreaterEqual(self.n_cells, 30)


if __name__ == "__main__":
    unittest.main()
