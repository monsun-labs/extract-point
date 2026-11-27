# 06 — Notebook Runtime Verification

**Phase:** 1B continuation  
**Date:** 2026-11-27  
**Branch tip at verification start:** `23d174fb9c7efdfd13e0e1499a4f4462412cc0b8`  
**Supersedes:** earlier PARTIAL note that full notebook runtime was not executed

---

## 1. Environment

| Item | Value |
|------|-------|
| Worktree | `C:\Users\yothu\tyo\monsun.io\monsun-labs\extract-point-phase-1b` |
| Interpreter | WSL `extract-point/.venv` Python 3.10.12 |
| CWD during run | `.../notebooks` (learner-like) |
| Sample | `data/era5_sample.nc` (local; SHA-256 matches Release) |
| Harness | `audit/phase-1b/_runtime_verify.py` (disposable; not part of learner UX) |
| Outputs | `audit/phase-1b/_runtime_out/` (gitignored) |

**Not used:** dependency installs, CDS, wget/git network (guarded), host Windows Python.

---

## 2. Commands

```bash
cd /mnt/c/Users/yothu/tyo/monsun.io/monsun-labs/extract-point-phase-1b
# after notebook resilience patches:
./.venv equivalent:
/mnt/c/Users/yothu/tyo/monsun.io/monsun-labs/extract-point/.venv/bin/python \
  audit/phase-1b/_runtime_verify.py
```

Final result: **`RUNTIME_EXIT=0`**

---

## 3. Execution results

| Metric | Count |
|--------|-------|
| Status OK (setup + code cells + assertions path) | **13** |
| Errors | **0** |
| Skipped | **23** (all markdown) |

All **code** cells executed successfully (including Step 0). Markdown cells were skipped by design (no code).

### Learner-flow coverage

| Step | Result |
|------|--------|
| 1. Environment/bootstrap (Step 0) | **OK** — sample already present; no download invoked |
| 2. Imports / setup constants | **OK** (cell 2) |
| 3. Sample load | **OK** |
| 4. Dataset inspection / indexing pedagogy | **OK** (cell 9) |
| 5. Coordinate selection | **OK** — nearest lat/lon indices 19/19 → 4.0°N, 108.0°E |
| 6. Hs extraction | **OK** (`swh` / `hs_m`) |
| 7. Tp extraction | **OK** (`tp` / `tp_s`) |
| 8. Wind extraction | **OK** (`u10`/`v10` → speed/dir) |
| 9. Plot generation | **OK** — quicklook + verify_*.png in `_runtime_out/` |
| 10. Final outputs | **OK** — CSV export + site statistics printed |

### Explicit assertions (post-run)

- `n_rows = 8784`
- columns include `hs_m`, `tp_s`, `wind_speed_ms`
- nearest summary: exact 4.0 / 108.0 on 39×39 grid

### Generated artifacts (disposable)

`benchmark_sample.csv/png`, `natuna_timeseries.csv`, `timeseries_quicklook.png`, `verify_hs.png`, `verify_tp.png`, `verify_wind.png`, `verify_extract_head.csv`

---

## 4. Executed vs skipped cells

- **Executed code cells:** 1 (Step 0), 2, 5, 9, 15, 17, 19, 22, 24, 26, 28, 30, 33 (+ harness assertions)
- **Skipped:** all markdown cells (0,3,4,6–8,10–14,16,18,20,21,23,25,27,29,31,32,34,35)
- **Not skipped for network:** Step 0 ran locally because sample size ≥ threshold; wget/git calls were blocked by the harness if attempted

---

## 5. Fixes applied after first failing runtime attempt

First harness run failed on cells that assumed Step 0 globals (`MIN_SAMPLE_BYTES`, `lat_arr`, `REPO_ROOT`) when Step 0 was skipped. Evidence-backed notebook hardening:

- Cell 2: local fallbacks for `MIN_SAMPLE_BYTES`, `REPO_ROOT`, `DATA_PATH`
- Cells 28/30: resolve `REPO_ROOT` if missing; tolerate non-IPython display

Re-run then produced **0 errors**.

---

## 6. Limitations

1. Not Jupyter UI “Run All”; cells executed via Python harness with Agg backend.
2. Colab-only branches of Step 0 (`git clone`, `pip install`) were not exercised (and were blocked from network).
3. Large-file live CDS benchmarks were not run; section 5.2 uses precomputed assets only.
4. IPython display was stubbed for headless execution.
