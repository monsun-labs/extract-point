# 03 — Test and Reproducibility Report

**Phase:** 1B  
**Environment:** WSL + existing repo `.venv` at `extract-point/.venv` (Python 3.10; xarray/netCDF4 already present)  
**No packages installed during this phase**

---

## 1. Tests executed

**Command:**

```bash
cd /mnt/c/Users/yothu/tyo/monsun.io/monsun-labs/extract-point-phase-1b
/mnt/c/Users/yothu/tyo/monsun.io/monsun-labs/extract-point/.venv/bin/python -m unittest discover -s tests -v
```

**Result:** `Ran 10 tests in ~11–13s` → **OK** (exit code 0)

| Test | Outcome |
|------|---------|
| `test_detect_dims_and_nearest` | PASS |
| `test_extract_point_and_wind` | PASS |
| `test_find_data_file` | PASS |
| `test_hardcoded_global_indices_out_of_range_for_toy` | PASS |
| `test_out_of_domain_raises` | PASS |
| `test_bootstrap_and_utils` (notebook structure) | PASS |
| `test_cell_count_reasonable` | PASS |
| `test_no_known_breakage` | PASS |
| `test_grid_and_vars` (sample metadata) | PASS |
| `test_sha256` (sample file) | PASS |

---

## 2. Other checks executed

| Check | Command / method | Outcome |
|-------|------------------|---------|
| Baseline SHAs | `git rev-parse main` / `origin/main` | Match `7006552` / `3416d57` |
| Worktree create | `git worktree add -b monsun/phase-1b-extract-point-stabilization … main` | Success |
| NetCDF header inspect | `netCDF4.Dataset` script via WSL | Success (see report 02) |
| Sample gitignore | `git check-ignore -v data/era5_sample.nc` | Ignored |
| Original workspace isolation | status on original clone | Still `add-extract-utils` @ `8f7b9d6`, only `?? data/era5_sample.nc` |

---

## 3. Tests / executions NOT run (and why)

| Item | Reason |
|------|--------|
| Full notebook “Run All” | Phase rules: avoid downloads/external services/uncontrolled workloads |
| CDS / ERA5 download scripts | Explicitly prohibited |
| Large / multi-GB benchmarks | Prohibited |
| `pip install` of requirements | No install approval; used existing venv |
| Windows native xarray | Not installed on host Python 3.12; WSL venv used instead |
| Colab live open | Network UX check not automated; URL constructed from verified org/repo |

---

## 4. Dependency / reproducibility status

| File | Role | Status |
|------|------|--------|
| `requirements-notebook.txt` | Learner/Colab | Present; unchanged pins/ranges |
| `requirements.txt` | Maintainer (cartopy/cdsapi) | Present |
| Release `v0.1-data` | Sample data | Documented + checksum in README/`data/README` |
| Local sample | Hardlink for tests | Not committed |

**Learner path (documented):** clone → wget Release asset → `pip install -r requirements-notebook.txt` → open notebook → Step 0 if needed.

**Gap:** host Windows Python lacks tutorial deps without using WSL/venv; documented as environment note, not fixed by installing.
