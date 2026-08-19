#!/usr/bin/env python3
"""Aggregate all app manifests into a single index.json."""
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
APPS_DIR = ROOT / "apps"
INDEX_PATH = ROOT / "index.json"


def build_index():
    entries = []
    for app_dir in sorted(APPS_DIR.iterdir()):
        if not app_dir.is_dir():
            continue
        manifest_path = app_dir / "manifest.json"
        if not manifest_path.exists():
            continue
        with open(manifest_path, "r", encoding="utf-8") as f:
            manifest = json.load(f)
        entries.append(manifest)

    index = {
        "store_version": 1,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "entries": entries,
    }

    with open(INDEX_PATH, "w", encoding="utf-8") as f:
        json.dump(index, f, indent=2, ensure_ascii=False)
        f.write("\n")

    print(f"index.json built with {len(entries)} entr{'ies' if len(entries) != 1 else 'y'}.")


if __name__ == "__main__":
    build_index()
