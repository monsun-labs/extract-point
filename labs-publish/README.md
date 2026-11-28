# labs-publish — notebook → website artifacts

Converts the committed tutorial notebook into Markdown + local media for
[Monsun Labs](https://monsun.io/labs/) **without executing** the notebook.

## Contract

| File | Role |
|------|------|
| `manifest.yaml` | Slug, URLs, sample metadata, media allowlist |
| `convert_notebook.py` | nbconvert MarkdownExporter + FilesWriter wrapper |
| `out/` | Dry-run / CI staging directory (gitignored) |

## Local dry-run

```bash
pip install -r labs-publish/requirements.txt
python labs-publish/convert_notebook.py
```

Artifacts land in `labs-publish/out/`:

- `body.md` — nbconvert Markdown (committed outputs only)
- `media/` — extracted outputs + allowlisted PNGs
- `provenance.yaml` — git SHA, body hash, `executed: false`
- `index.md` — only when `website.replace_index: true` in the manifest

Apply into a local website checkout:

```bash
python labs-publish/apply_to_website.py --website-root /path/to/monsun-labs.github.io
```

CI: `.github/workflows/labs-publish.yml` calls the reusable workflow on
`monsun-labs.github.io` and opens/updates branch `publish/<slug>` (no merge).

Requires secret `LABS_PUBLISH_TOKEN` (GitHub App installation token preferred;
fine-grained PAT owned by tyorus is an interim option). See website
[`LABS_PUBLISH.md`](https://github.com/monsun-labs/monsun-labs.github.io/blob/main/LABS_PUBLISH.md).

## Rules

- Source of truth remains the `.ipynb` with committed outputs.
- No `--execute` / ExecutePreprocessor.
- Only media paths listed in the manifest are copied.
- Website PRs are opened by automation; humans merge (Policy B).
- Pilot keeps curated website `index.md` (`replace_index: false`).
