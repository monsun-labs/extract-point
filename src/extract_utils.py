"""
extract_utils.py — Monsun Labs · extract-point

Reusable helpers for ERA5 and gridded NetCDF point extraction.

Longitude note
--------------
Nearest-neighbour selection uses absolute difference on the coordinate values
as stored in the file. This is correct for regional extracts that use a
consistent convention (e.g. Natuna at 108°E on a 0–360 or −180–180 grid that
already contains 108). It does **not** wrap across the antimeridian
(e.g. requesting −170 on a 0–360 grid, or vice versa). Callers working near
±180° must align the request longitude with the file's convention first.
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import xarray as xr

DEFAULT_RENAME = {
    "swh": "hs_m",
    "tp": "tp_s",
    "mwd": "wave_dir_deg",
    "shts": "swell_hs_m",
    "mdts": "swell_dir_deg",
    "mpts": "swell_tp_s",
    "u10": "u10_ms",
    "v10": "v10_ms",
}

LAT_CANDIDATES = ("latitude", "lat", "y")
LON_CANDIDATES = ("longitude", "lon", "x")
TIME_CANDIDATES = ("time", "valid_time")
WAVE_VAR_CANDIDATES = ("swh", "Hs", "hs", "VHM0")


def find_data_file(*candidates: str | Path) -> Path:
    """Return the first existing path from candidates, or raise FileNotFoundError."""
    for candidate in candidates:
        path = Path(candidate)
        if path.exists():
            return path
    raise FileNotFoundError(
        f"None of the candidate paths exist: {[str(c) for c in candidates]}"
    )


def detect_dims(ds: xr.Dataset) -> tuple[str, str, str | None]:
    """Return (lat_dim, lon_dim, time_dim) from common naming conventions."""
    lat_dim = next((name for name in LAT_CANDIDATES if name in ds.dims or name in ds.coords), None)
    lon_dim = next((name for name in LON_CANDIDATES if name in ds.dims or name in ds.coords), None)
    time_dim = next((name for name in TIME_CANDIDATES if name in ds.dims), None)
    if lat_dim is None or lon_dim is None:
        raise ValueError(
            f"Could not detect lat/lon dims in {list(ds.dims)} / {list(ds.coords)}"
        )
    return lat_dim, lon_dim, time_dim


def detect_wave_var(ds: xr.Dataset, var: str | None = None) -> str:
    """Pick the primary wave-height variable for benchmarking."""
    if var and var in ds.data_vars:
        return var
    for name in WAVE_VAR_CANDIDATES:
        if name in ds.data_vars:
            return name
    if ds.data_vars:
        return next(iter(ds.data_vars))
    raise ValueError("No data variables found in dataset")


def nearest_indices(
    ds: xr.Dataset,
    lat: float,
    lon: float,
    *,
    lat_dim: str | None = None,
    lon_dim: str | None = None,
) -> tuple[int, int, str, str]:
    """
    Return (lat_idx, lon_idx, lat_dim, lon_dim) for the nearest grid cell.

    Uses absolute difference on stored coordinates (no antimeridian wrap).
    """
    detected_lat, detected_lon, _ = detect_dims(ds)
    lat_dim = lat_dim or detected_lat
    lon_dim = lon_dim or detected_lon
    lat_vals = np.asarray(ds[lat_dim].values)
    lon_vals = np.asarray(ds[lon_dim].values)
    if lat_vals.size == 0 or lon_vals.size == 0:
        raise ValueError("Latitude/longitude coordinates are empty")
    lat_idx = int(np.abs(lat_vals - lat).argmin())
    lon_idx = int(np.abs(lon_vals - lon).argmin())
    return lat_idx, lon_idx, lat_dim, lon_dim


def describe_nearest_point(
    ds: xr.Dataset,
    lat: float,
    lon: float,
    *,
    lat_dim: str | None = None,
    lon_dim: str | None = None,
) -> dict[str, float | int | str]:
    """Human-inspectable summary of the nearest grid point selection."""
    lat_idx, lon_idx, lat_name, lon_name = nearest_indices(
        ds, lat, lon, lat_dim=lat_dim, lon_dim=lon_dim
    )
    lat_sel = float(ds[lat_name].values[lat_idx])
    lon_sel = float(ds[lon_name].values[lon_idx])
    return {
        "requested_lat": float(lat),
        "requested_lon": float(lon),
        "lat_dim": lat_name,
        "lon_dim": lon_name,
        "lat_idx": lat_idx,
        "lon_idx": lon_idx,
        "selected_lat": lat_sel,
        "selected_lon": lon_sel,
        "lat_delta_deg": abs(lat_sel - float(lat)),
        "lon_delta_deg": abs(lon_sel - float(lon)),
        "grid_n_lat": int(ds.sizes[lat_name]),
        "grid_n_lon": int(ds.sizes[lon_name]),
    }


def extract_point(
    nc_path: str | Path,
    lat: float,
    lon: float,
    variables: list[str] | None = None,
    method: str = "nearest",
    chunks: dict | None = None,
    rename: dict[str, str] | None = DEFAULT_RENAME,
    lat_dim: str | None = None,
    lon_dim: str | None = None,
) -> pd.DataFrame:
    """
    Extract a time series at (lat, lon) from a NetCDF file.

    Parameters
    ----------
    nc_path   : Path to the NetCDF file.
    lat, lon  : Target coordinates (degrees), in the same longitude convention
                as the file (no automatic ±180 wrap).
    variables : Variable names to extract (default: all data vars).
    method    : 'nearest' or 'linear' (bilinear interpolation).
    chunks    : Dask chunks dict, e.g. {"time": 500}. None = no Dask.
    rename    : Column rename map applied after extraction. None = keep raw names.
    lat_dim   : Override latitude dimension name (auto-detected if None).
    lon_dim   : Override longitude dimension name (auto-detected if None).

    Returns
    -------
    pd.DataFrame indexed by datetime.
    """
    ds = xr.open_dataset(nc_path, chunks=chunks)
    try:
        detected_lat, detected_lon, _ = detect_dims(ds)
        lat_dim = lat_dim or detected_lat
        lon_dim = lon_dim or detected_lon
        variables = variables or list(ds.data_vars)

        # Validate request is not wildly outside the grid (clear learner error).
        lat_min = float(np.min(ds[lat_dim].values))
        lat_max = float(np.max(ds[lat_dim].values))
        lon_min = float(np.min(ds[lon_dim].values))
        lon_max = float(np.max(ds[lon_dim].values))
        # Allow a one-cell tolerance beyond edges for nearest selection messaging.
        pad_lat = float(np.median(np.abs(np.diff(np.asarray(ds[lat_dim].values))))) if ds.sizes[lat_dim] > 1 else 0.0
        pad_lon = float(np.median(np.abs(np.diff(np.asarray(ds[lon_dim].values))))) if ds.sizes[lon_dim] > 1 else 0.0
        if not (lat_min - pad_lat <= lat <= lat_max + pad_lat and lon_min - pad_lon <= lon <= lon_max + pad_lon):
            raise ValueError(
                f"Requested point ({lat}, {lon}) is outside the dataset domain "
                f"lat[{lat_min}, {lat_max}] lon[{lon_min}, {lon_max}] "
                f"(no antimeridian wrap is applied)."
            )

        if method == "linear":
            point = ds[variables].interp(**{lat_dim: lat, lon_dim: lon})
        else:
            point = ds[variables].sel(**{lat_dim: lat, lon_dim: lon}, method=method)

        drop_cols = [lat_dim, lon_dim, "number", "expver", "depth", "surface"]
        df = point.compute().to_dataframe().drop(columns=drop_cols, errors="ignore")
        df.index = pd.to_datetime(df.index)
        df.index.name = "datetime"

        if rename:
            df = df.rename(columns={k: v for k, v in rename.items() if k in df.columns})

        return df
    finally:
        ds.close()


def add_wind_speed(df: pd.DataFrame, u_col: str = "u10_ms", v_col: str = "v10_ms") -> pd.DataFrame:
    """Add wind_speed_ms and wind_dir_deg columns (meteorological convention)."""
    result = df.copy()
    result["wind_speed_ms"] = np.sqrt(result[u_col] ** 2 + result[v_col] ** 2)
    result["wind_dir_deg"] = (270 - np.degrees(np.arctan2(result[v_col], result[u_col]))) % 360
    return result


def quick_stats(df: pd.DataFrame, var: str) -> pd.Series:
    """Return key percentile statistics for a variable."""
    series = df[var].dropna()
    return pd.Series(
        {
            "mean": series.mean(),
            "std": series.std(),
            "p50": series.quantile(0.50),
            "p90": series.quantile(0.90),
            "p95": series.quantile(0.95),
            "p99": series.quantile(0.99),
            "max": series.max(),
            "n": len(series),
        },
        name=var,
    )
