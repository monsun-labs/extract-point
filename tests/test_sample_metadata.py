"""Metadata checks against local era5_sample.nc when present (no downloads)."""
from __future__ import annotations

import hashlib
import unittest
from pathlib import Path

from netCDF4 import Dataset
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
SAMPLE = ROOT / "data" / "era5_sample.nc"
EXPECTED_SHA256 = "f11e80d5e7a7769ff26f19ebf2f842839afa3a801f750c32cbbb341b52e1aab4"


@unittest.skipUnless(SAMPLE.exists(), "data/era5_sample.nc not present")
class SampleMetadataTests(unittest.TestCase):
    def test_sha256(self) -> None:
        h = hashlib.sha256()
        with SAMPLE.open("rb") as fh:
            for chunk in iter(lambda: fh.read(1024 * 1024), b""):
                h.update(chunk)
        self.assertEqual(h.hexdigest(), EXPECTED_SHA256)

    def test_grid_and_vars(self) -> None:
        ds = Dataset(SAMPLE, "r")
        try:
            self.assertEqual(len(ds.dimensions["time"]), 8784)
            self.assertEqual(len(ds.dimensions["latitude"]), 39)
            self.assertEqual(len(ds.dimensions["longitude"]), 39)
            for name in ("u10", "v10", "swh", "tp", "mwd", "shts", "mdts", "mpts"):
                self.assertIn(name, ds.variables)
            lat = np.asarray(ds.variables["latitude"][:])
            lon = np.asarray(ds.variables["longitude"][:])
            self.assertTrue(np.all(np.diff(lat) > 0))
            self.assertTrue(np.all(np.diff(lon) > 0))
            self.assertAlmostEqual(float(np.median(np.diff(lon))), 0.25, places=5)
            lat_idx = int(np.abs(lat - 4.0).argmin())
            lon_idx = int(np.abs(lon - 108.0).argmin())
            self.assertEqual(float(lat[lat_idx]), 4.0)
            self.assertEqual(float(lon[lon_idx]), 108.0)
            self.assertFalse(42 < lat.size)
            self.assertFalse(864 < lon.size)
            self.assertEqual(ds.variables["swh"].units, "m")
            self.assertEqual(ds.variables["tp"].units, "s")
            self.assertEqual(ds.variables["u10"].units, "m s**-1")
        finally:
            ds.close()


if __name__ == "__main__":
    unittest.main()
