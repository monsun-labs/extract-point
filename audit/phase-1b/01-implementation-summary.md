# 01 — Implementation Summary

**Phase:** 1B — Extract Point Restoration & Stabilization  
**Date:** 2026-11-27  
**Working branch:** `monsun/phase-1b-extract-point-stabilization`  
**Worktree:** `C:\Users\yothu\tyo\monsun.io\monsun-labs\extract-point-phase-1b`  
**Baseline commit:** `70065526f034f3350c249b227c73b2987c39e7be` (local `main`)

---

## 1. What was restored / changed

| Area | Action |
|------|--------|
| Branch isolation | New branch from local `main` in a **separate git worktree** (original workspace left on `add-extract-utils`) |
| Tutorial body | Preserved main-line notebook, utils, benchmarks, requirements-notebook, Release data flow |
| `src/extract_utils.py` | Rebranded header; added `nearest_indices`, `describe_nearest_point`; domain-bounds check; lon-wrap limitation documented; ensure dataset `close()` |
| Docs | README + `data/README.md` updated to Monsun URLs and **verified** sample metadata (39×39 @ 0.25°, not outdated 20×20 @ 0.5° table) |
| Notebook | Bootstrap/Release/GitHub/LinkedIn/plot titles rebranded; sample-size wording corrected; removed stored stderr path containing `nusawave-labs` |
| Benchmarks | Plot titles → Monsun Labs |
| Tests | Added `tests/` with synthetic utility tests, sample metadata tests, notebook structure tests |
| LICENSE | **Unchanged** (copyright holder remains as on baseline) |

## 2. Files added / modified / removed

### Modified
- `README.md`
- `data/README.md`
- `src/extract_utils.py`
- `notebooks/extract_point.ipynb`
- `benchmarks/benchmark.py`
- `benchmarks/generate_assets.py`

### Added
- `tests/test_extract_utils.py`
- `tests/test_sample_metadata.py`
- `tests/test_notebook_structure.py`
- `audit/phase-1b/*.md` (this report set)

### Removed
- None of the main-line tutorial capabilities
- Temporary inspection scripts under `audit/` cleaned before finalize

### Not committed
- `data/era5_sample.nc` (hardlinked for local tests; still gitignored)

## 3. Important decisions

1. **Baseline:** local `main` @ `7006552`, not WIP.
2. **Grid docs follow the Release file**, not the download-script defaults (script still defaults to 20×20 / 0.5° regenerate recipe — documented as drift).
3. **No antimeridian lon wrap** implemented; limitation documented + out-of-domain `ValueError`.
4. **Colab URL** points at `monsun-labs/extract-point` `main` with an explicit note that content matches this branch only after merge.
5. **README avoids a conflicting © Monsun line** while LICENSE still says Nusawave Labs.
6. **No dependency installs** performed; tests used the existing Linux `.venv` via WSL.
