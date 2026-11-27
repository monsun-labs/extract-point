# 07 — Downloader and Release Consistency

**Phase:** 1B continuation  
**Date:** 2026-11-27  
**Downloader inspected:** `scripts/download_era5.py` (static only — **not executed**, no CDS calls)

---

## 1. Release sample characteristics (verified earlier + unchanged)

| Property | Release `v0.1-data` / local `era5_sample.nc` |
|----------|-----------------------------------------------|
| Size | 118,466,500 bytes |
| SHA-256 | `f11e80d5e7a7769ff26f19ebf2f842839afa3a801f750c32cbbb341b52e1aab4` |
| Dims | time 8784 × lat 39 × lon 39 |
| Coord spacing | median **0.25°** |
| Time | 2024-01-01 → 2024-12-31 hourly |
| Vars | `u10`, `v10`, `swh`, `tp`, `mwd`, `shts`, `mdts`, `mpts` |
| Path for learners | GitHub Release download (not git commit) |

---

## 2. Downloader default configuration

| Setting | Default in `download_era5.py` |
|---------|-------------------------------|
| Dataset | `reanalysis-era5-single-levels` |
| Variables | same short-name set as tutorial (`swh`…`v10`) |
| Center | 4°N, 108°E |
| `DEFAULT_YEARS` | **1** ending `DEFAULT_END_YEAR=2024` |
| `DEFAULT_GRID_POINTS` | **20** |
| `GRID_SPACING_DEG` | **0.5** (wave-resolution box math) |
| Expected shape (approx) | ~20 × 20 at 0.5° |
| Output | `data/era5_sample.nc` |
| Modes | `--sample` (tiny), `--benchmark` (10 yr large) |

Geographic box uses `buffer_for_grid(n)` = `(n-1)*0.5/2` degrees half-width.

---

## 3. Do they serve the same purpose?

**No — and that is acceptable if documented.**

| Artifact | Role |
|----------|------|
| Release `v0.1-data` | **Learner teaching file** — pinned bytes for Colab/local tutorial |
| `download_era5.py` defaults | **Maintainer regenerate/custom CDS tool** — different recipe; may produce a related but non-identical NetCDF |

They share variable names and Natuna focus, but **not** identical dimensions or byte identity.

---

## 4. Differences explained

1. Release file coordinates are **39×39 @ 0.25°** (wind-like mesh; wave GRIB attrs still mention 0.5° native).
2. Downloader box math assumes **0.5°** spacing and **20** points → ~20×20.
3. Historical regenerate path / CDS packaging likely produced the Release asset under a different grid choice than today’s defaults.
4. Overwriting `data/era5_sample.nc` via the script without republishing Release would **desync** tutorial docs and Colab.

---

## 5. Fixes applied (documentation / CLI clarity)

Updated `scripts/download_era5.py`:

- Module docstring now states learners must use Release `v0.1-data`.
- Explicit warning that defaults **will not** reproduce Release dimensions.
- Argparse description mirrors that warning.
- Points maintainers to `data/README.md`.

No downloader execution. No change to CDS request logic beyond messaging (safer than silently changing grid defaults without a new Release plan).

---

## 6. Remaining recommendations (future phase)

1. Optionally add `--match-release` preset once a reproducible recipe for 39×39/0.25° is confirmed.
2. Website Extract Point page should describe Release sample (39×39 @ 0.25°), not downloader defaults.
3. Keep large downloads behind `--benchmark` / `--force` (already gated by size estimate).
