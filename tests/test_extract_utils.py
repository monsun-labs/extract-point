"""Controlled unit tests for extract_utils (synthetic data; no network)."""
from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

import numpy as np
import pandas as pd
import xarray as xr

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from extract_utils import (  # noqa: E402
    add_wind_speed,
    describe_nearest_point,
    detect_dims,
    extract_point,
    find_data_file,
    nearest_indices,
    quick_stats,
)


def _synthetic_dataset() -> xr.Dataset:
    lats = np.array([-1.0, 0.0, 1.0, 2.0, 3.0, 4.0, 5.0])
    lons = np.array([106.0, 107.0, 108.0, 109.0, 110.0])
    times = pd.date_range("2024-01-01", periods=6, freq="h")
    rng = np.random.default_rng(0)
    shape = (times.size, lats.size, lons.size)
    return xr.Dataset(
        {
            "swh": (("time", "latitude", "longitude"), rng.random(shape).astype("float32")),
            "tp": (("time", "latitude", "longitude"), (rng.random(shape) * 10).astype("float32")),
            "u10": (("time", "latitude", "longitude"), (rng.normal(0, 3, shape)).astype("float32")),
            "v10": (("time", "latitude", "longitude"), (rng.normal(0, 3, shape)).astype("float32")),
        },
        coords={"time": times, "latitude": lats, "longitude": lons},
    )


class ExtractUtilsTests(unittest.TestCase):
    def test_find_data_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "sample.nc"
            path.write_text("x", encoding="utf-8")
            found = find_data_file(Path(tmp) / "missing.nc", path)
            self.assertEqual(found, path)
            with self.assertRaises(FileNotFoundError):
                find_data_file(Path(tmp) / "nope.nc")

    def test_detect_dims_and_nearest(self) -> None:
        ds = _synthetic_dataset()
        lat_dim, lon_dim, time_dim = detect_dims(ds)
        self.assertEqual((lat_dim, lon_dim, time_dim), ("latitude", "longitude", "time"))
        lat_idx, lon_idx, _, _ = nearest_indices(ds, 4.0, 108.0)
        self.assertEqual(lat_idx, 5)
        self.assertEqual(lon_idx, 2)
        info = describe_nearest_point(ds, 4.0, 108.0)
        self.assertEqual(info["selected_lat"], 4.0)
        self.assertEqual(info["selected_lon"], 108.0)

    def test_out_of_domain_raises(self) -> None:
        ds = _synthetic_dataset()
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "toy.nc"
            ds.to_netcdf(path)
            with self.assertRaises(ValueError):
                extract_point(path, lat=50.0, lon=108.0)

    def test_extract_point_and_wind(self) -> None:
        ds = _synthetic_dataset()
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "toy.nc"
            ds.to_netcdf(path)
            df = extract_point(path, 4.0, 108.0)
            self.assertIn("hs_m", df.columns)
            self.assertIn("tp_s", df.columns)
            self.assertIn("u10_ms", df.columns)
            self.assertEqual(len(df), 6)
            out = add_wind_speed(df)
            self.assertIn("wind_speed_ms", out.columns)
            self.assertIn("wind_dir_deg", out.columns)
            stats = quick_stats(out, "hs_m")
            self.assertEqual(int(stats["n"]), 6)

    def test_hardcoded_global_indices_out_of_range_for_toy(self) -> None:
        ds = _synthetic_dataset()
        self.assertFalse(42 < ds.sizes["latitude"])
        self.assertFalse(864 < ds.sizes["longitude"])


if __name__ == "__main__":
    unittest.main()
