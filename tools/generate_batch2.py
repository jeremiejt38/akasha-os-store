#!/usr/bin/env python3
"""Generate manifest.json + icon.png for the second batch of apps (plan
f4e069bb phase 2). Run from the repo root: python3 tools/generate_batch2.py
"""
import json
import subprocess
import sys
from datetime import date, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from seed_data import APPS  # noqa: E402

REPO_ROOT = Path(__file__).parent.parent
TODAY = date.today().isoformat()


def build_manifest(app):
    manifest = {
        "id": app["id"],
        "name": app["name"],
        "version": "1.0.0",
        "category": app["category"],
        "description": app["description"],
        "icon": "icon.png",
        "install": app["install"],
        "legal_notice": app["legal_notice"],
        "min_os_version": "12.0",
        "maintainer": "jeremiejt38",
        "last_verified": TODAY,
    }
    return manifest


def main():
    created = []
    for app in APPS:
        app_dir = REPO_ROOT / "apps" / app["id"]
        app_dir.mkdir(parents=True, exist_ok=True)
        manifest_path = app_dir / "manifest.json"
        if manifest_path.exists():
            print(f"skip (exists): {app['id']}")
            continue
        manifest = build_manifest(app)
        with open(manifest_path, "w", encoding="utf-8") as f:
            json.dump(manifest, f, ensure_ascii=False, indent=2)
            f.write("\n")
        icon_path = app_dir / "icon.png"
        subprocess.run(
            [sys.executable, str(REPO_ROOT / "tools" / "generate_placeholder_icon.py"),
             app["id"], "-o", str(icon_path)],
            check=True, cwd=REPO_ROOT)
        created.append(app["id"])
        print(f"created: {app['id']}")
    print(f"\n{len(created)} manifest(s) created.")


if __name__ == "__main__":
    main()
