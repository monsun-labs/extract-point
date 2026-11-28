#!/usr/bin/env python3
"""Copy labs-publish/out artifacts into a local website repo checkout.

Does not commit, push, or open PRs. Used by CI after conversion and for local dry-runs.

Usage:
  python labs-publish/convert_notebook.py
  python labs-publish/apply_to_website.py --website-root /path/to/monsun-labs.github.io
"""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=REPO_ROOT / "labs-publish" / "manifest.yaml")
    parser.add_argument("--out", type=Path, default=REPO_ROOT / "labs-publish" / "out")
    parser.add_argument("--website-root", type=Path, required=True)
    args = parser.parse_args(argv)

    manifest = yaml.safe_load(args.manifest.read_text(encoding="utf-8"))
    website = manifest["website"]
    docs_rel = website["docs_relpath"]
    media_dirname = website.get("media_dirname", "media")
    body_name = website.get("generated_body", "body.md")
    replace_index = bool(website.get("replace_index", False))

    out = args.out.resolve()
    dest_dir = (args.website_root.resolve() / docs_rel)
    if not dest_dir.parent.is_dir():
        raise SystemExit(f"Website tutorials parent missing: {dest_dir.parent}")

    dest_dir.mkdir(parents=True, exist_ok=True)
    body_src = out / body_name
    if not body_src.is_file():
        raise SystemExit(f"Missing converted body: {body_src}")
    shutil.copy2(body_src, dest_dir / body_name)

    media_src = out / media_dirname
    media_dest = dest_dir / media_dirname
    if media_dest.exists():
        shutil.rmtree(media_dest)
    if media_src.is_dir():
        shutil.copytree(media_src, media_dest)

    if replace_index:
        index_src = out / website.get("landing_index", "index.md")
        if not index_src.is_file():
            raise SystemExit(f"replace_index=true but missing {index_src}")
        shutil.copy2(index_src, dest_dir / index_src.name)

    prov_src = out / "provenance.yaml"
    if prov_src.is_file():
        shutil.copy2(prov_src, dest_dir / "provenance.yaml")

    print(f"Applied publish artifacts to {dest_dir}")
    print(f"  replace_index={replace_index}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
