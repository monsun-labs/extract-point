# 04 — Brand and Website Readiness

**Phase:** 1B  
**Canonical site URL (unchanged):** `https://monsun.io/labs/`

---

## 1. Rebrand changes applied (working branch)

| Location | Change |
|----------|--------|
| README | Monsun Labs + `monsun.io/labs/`; GitHub/Colab/Release URLs → `monsun-labs/extract-point` |
| Notebook bootstrap | `REPO_URL` + Release URL → `monsun-labs` |
| Notebook titles / closing | Monsun Labs; LinkedIn → `company/monsunic` |
| `src/extract_utils.py` header | Monsun Labs |
| Benchmark / generate_assets titles | Monsun Labs |
| `data/README.md` | Monsun Release URLs + ECMWF/CDS attribution |

## 2. Intentionally unchanged

| Item | Reason |
|------|--------|
| `LICENSE` copyright line (`Nusawave Labs`) | Explicit Phase 1B restriction — pending ownership confirmation |
| Git history / remote URL host `nusawave-labs` | No remote mutation authorized |
| Published `origin/main` content | Not modified |

## 3. Remaining attribution / copyright questions

1. When may LICENSE copyright holder become Monsun Labs?
2. Should README carry an explicit © line once ownership is confirmed?
3. Confirm LinkedIn `monsunic` remains the public company page (used to match website).

## 4. Website integration checklist (no website edits in 1B)

| Item | Status / recommendation |
|------|-------------------------|
| Tutorial title | Point Extraction / extract-point |
| Short description | Extract Hs, Tp, and wind at a point from ERA5 without loading the full grid |
| Canonical docs URL | `https://monsun.io/labs/tutorials/extract-point/` |
| README links | Point to `monsun.io/labs/` and `github.com/monsun-labs/extract-point` |
| Colab CTA | Ready **after merge to `main`**; until then badge opens published main (noted in README) |
| Media for site | Optional: `data/download_area.png`, `data/benchmark/era5_large_benchmark.png` |
| Safe scientific claims | See report 02 §5 — update site “20×20 / 0.5° sample” wording to **39×39 / 0.25° file coords** + GRIB nuance |
| Sample size claim | ~118 MB, year 2024 |
| Attribution | ECMWF / Copernicus CDS |
| Dependencies listed on site | Keep `requirements-notebook.txt` + Release bootstrap story |

## 5. Blockers before website sync

1. Merge/publish of this branch to GitHub `main` (not done in 1B).
2. Update website Extract Point page grid/resolution table to match verified metadata.
3. LICENSE ownership decision if public legal text must match Monsun branding everywhere.
