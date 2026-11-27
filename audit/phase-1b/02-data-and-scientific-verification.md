# 02 — Data and Scientific Verification

**Phase:** 1B  
**Sample path inspected:** `data/era5_sample.nc` (hardlink to original untracked file)  
**Tool:** existing WSL `.venv` + `netCDF4.Dataset` (header/coordinate reads)  
**No CDS/ERA5 downloads performed**

---

## 1. Byte identity

| Check | Result |
|-------|--------|
| Size | 118,466,500 bytes |
| SHA-256 | `f11e80d5e7a7769ff26f19ebf2f842839afa3a801f750c32cbbb341b52e1aab4` |
| Matches Release digest (Phase 0/1A) | **Yes** |

Byte identity ≠ full scientific validation; it only confirms this is the Release asset bytes.

---

## 2. NetCDF metadata findings

| Item | Value |
|------|-------|
| Format | NETCDF4 |
| Dims | `time=8784`, `latitude=39`, `longitude=39` |
| Data vars | `u10`, `v10`, `swh`, `tp`, `mwd`, `shts`, `mdts`, `mpts` |
| Coords | `time`, `latitude`, `longitude`, plus `number`, `expver` |

### Coordinates

| Coord | Units / notes | Range / step |
|-------|---------------|--------------|
| `latitude` | `degrees_north`; array **monotonic increasing** | −0.75 → 8.75; median step **0.25°** |
| `longitude` | `degrees_east` | 103.25 → 112.75; median step **0.25°** |
| `time` | `seconds since 1970-01-01`, proleptic_gregorian | first `1704067200` (2024-01-01 00:00 UTC), last `1735686000` (2024-12-31 23:00 UTC) |

Attr note: `latitude` carries `stored_direction=decreasing` but the stored array increases — treat **array values** as authoritative for indexing.

### Variable attributes (evidence for units / names)

| Var | `long_name` | `units` | `_FillValue` |
|-----|-------------|---------|--------------|
| `swh` | Significant height of combined wind waves and swell | `m` | `nan` |
| `tp` | Peak wave period | `s` | `nan` |
| `mwd` | Mean wave direction | `Degree true` | `nan` |
| `shts` | Significant height of total swell | `m` | `nan` |
| `mdts` | Mean direction of total swell | `degrees` | `nan` |
| `mpts` | Mean period of total swell | `s` | `nan` |
| `u10` | 10 metre U wind component | `m s**-1` | `nan` |
| `v10` | 10 metre V wind component | `m s**-1` | `nan` |

### GRIB increment metadata (not array shape)

- Wind vars: GRIB `i/jDirectionIncrementInDegrees = 0.25`, native Ny/Nx 39.
- Wave vars: GRIB increment **0.5°**, native Ny/Nx 19 — but stored on the shared 39×39 dims in this file.

### Nearest point (4°N, 108°E)

| Metric | Value |
|--------|-------|
| `lat_idx` / `lon_idx` | 19 / 19 |
| Selected coords | exactly 4.0 / 108.0 |
| Index 42 / 864 in range? | **False / False** |

---

## 3. Comparison to prior documentation

| Prior claim | Actual file | Resolution in 1B |
|-------------|-------------|------------------|
| 20×20 @ 0.5° | 39×39 @ 0.25° coords | Docs/`data/README` updated |
| ~120 MB / 2024 | ~118 MB / 2024 hourly (8784) | Aligned |
| Hs/Tp/wind via `swh`/`tp`/`u10`/`v10` | Present with units above | Supported by attrs |
| WIP `0.25°` as “wrong” vs docs | File coords **are** 0.25°; wave GRIB still 0.5° | Clarified dual meaning |
| Magic indices 42/864 | Out of range | Main-line notebook already uses `lat_idx`; tests assert |

---

## 4. Remaining scientific uncertainties

1. **Physical validation** of values (plausibility of Hs/Tp/wind magnitudes over Natuna) — **not** performed (no full timeseries QA).
2. **Why** wave fields appear on a 0.25° mesh while GRIB says 0.5° — interpolation/regrid history not reconstructed; documented as metadata tension.
3. **Regenerate parity:** current `scripts/download_era5.py` defaults will not reproduce this asset’s shape.
4. **Antimeridian** behaviour — intentionally unsupported; documented.
5. Full notebook end-to-end execution against the sample — **not** run in 1B (by design); utility + metadata tests cover critical pieces.

---

## 5. Claims that are safe vs unsafe for website

**Safe (metadata-backed):**
- Sample is ERA5-derived NetCDF with listed variables and units.
- Regional Natuna extract; exact grid point at 4°N, 108°E exists.
- ~118 MB; calendar year 2024 hourly.
- Prefer lazy xarray selection over loading full arrays.

**Unsafe / needs nuance:**
- “20×20 at 0.5° sample grid” (false for this asset).
- Implying all variables are native 0.5° in-array without mentioning remapping/GRIB notes.
- Claiming runtime performance numbers without re-running benchmarks on this machine.
