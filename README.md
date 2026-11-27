# extract-point
### Stop Crashing Your Laptop: How to Extract ERA5 Point Data in Under 10 Seconds

**Part of [Monsun Labs](https://monsun.io/labs/)**

## Quick Start (Google Colab)

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/monsun-labs/extract-point/blob/main/notebooks/extract_point.ipynb)

1. Click **Open in Colab** above
2. **Runtime → Run all** (or run the first cell, then Run all)
3. Done — no terminal, no `git clone`, no CDS account

The notebook clones this repo, installs dependencies, and downloads the sample NetCDF from a [GitHub Release](https://github.com/monsun-labs/extract-point/releases/tag/v0.1-data) automatically.

> **Note:** Until this branch is merged to `main`, the Colab badge opens the current published `main` notebook. After merge, it will reflect the stabilized Monsun Labs tutorial.

## Quick Start (local)

```bash
git clone https://github.com/monsun-labs/extract-point.git
cd extract-point
wget -q -O data/era5_sample.nc \
  https://github.com/monsun-labs/extract-point/releases/download/v0.1-data/era5_sample.nc
pip install -r requirements-notebook.txt   # tutorial only
# pip install -r requirements.txt        # + cartopy/cdsapi for maintainer scripts
jupyter notebook notebooks/extract_point.ipynb
```

Run the **Step 0** bootstrap cell if the sample file is missing.

Expected sample checksum (SHA-256):

```
f11e80d5e7a7769ff26f19ebf2f842839afa3a801f750c32cbbb341b52e1aab4
```

## What You'll Learn
- Lazy vs eager loading (the concept that saves your RAM)
- sel vs isel vs interp — when to use each
- Performance benchmarks across 4 extraction engines
- Clean export to CSV for downstream analysis

## Data
Uses ERA5 reanalysis (ECMWF / Copernicus CDS) — open access, free to download.
Pre-sliced sample (~118 MB, calendar year 2024) for hands-on work; pre-computed benchmark charts for large-file comparisons (see `data/benchmark/`).

See [`data/README.md`](data/README.md) for verified grid dimensions, variables, and units from the Release asset.

## License
MIT — use freely, attribution appreciated. See [`LICENSE`](LICENSE) for the copyright notice and terms (copyright holder unchanged in Phase 1B pending ownership confirmation).
