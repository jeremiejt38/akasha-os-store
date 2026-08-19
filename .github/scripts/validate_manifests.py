#!/usr/bin/env python3
"""Validate every apps/<id>/manifest.json against the JSON schema."""
import json
import os
import sys
from pathlib import Path

import jsonschema
import requests

ROOT = Path(__file__).resolve().parents[2]
SCHEMA_PATH = ROOT / "schema" / "manifest.schema.json"
APPS_DIR = ROOT / "apps"


def load_json(path: Path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def validate_manifests():
    schema = load_json(SCHEMA_PATH)
    errors = []
    checked = 0

    for app_dir in sorted(APPS_DIR.iterdir()):
        if not app_dir.is_dir():
            continue
        manifest_path = app_dir / "manifest.json"
        icon_path = app_dir / "icon.png"

        if not manifest_path.exists():
            errors.append(f"{app_dir.name}: missing manifest.json")
            continue

        try:
            manifest = load_json(manifest_path)
        except json.JSONDecodeError as exc:
            errors.append(f"{app_dir.name}: invalid JSON ({exc})")
            continue

        try:
            jsonschema.validate(manifest, schema)
        except jsonschema.ValidationError as exc:
            errors.append(f"{app_dir.name}: schema error: {exc.message}")
            continue

        if not icon_path.exists():
            errors.append(f"{app_dir.name}: missing icon.png")
            continue

        icon_size = icon_path.stat().st_size
        if icon_size > 100 * 1024:
            errors.append(f"{app_dir.name}: icon.png exceeds 100 KiB ({icon_size} bytes)")
            continue

        # Verify source_url responds (HEAD only)
        source_url = manifest["install"]["source_url"]
        try:
            resp = requests.head(source_url, timeout=30, allow_redirects=True)
            if resp.status_code >= 400:
                errors.append(f"{app_dir.name}: source_url returned {resp.status_code}")
                continue
        except requests.RequestException as exc:
            errors.append(f"{app_dir.name}: source_url unreachable ({exc})")
            continue

        # For zip-url, verify sha256
        if manifest["install"]["type"] == "zip-url":
            expected = manifest["install"]["sha256"].lower()
            try:
                r = requests.get(source_url, timeout=60)
                r.raise_for_status()
                import hashlib

                actual = hashlib.sha256(r.content).hexdigest()
                if actual != expected:
                    errors.append(
                        f"{app_dir.name}: sha256 mismatch (expected {expected}, got {actual})"
                    )
                    continue
            except requests.RequestException as exc:
                errors.append(f"{app_dir.name}: zip-url download failed ({exc})")
                continue

        checked += 1

    if errors:
        print("Validation errors:", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        sys.exit(1)

    print(f"{checked} manifest(s) validated successfully.")


if __name__ == "__main__":
    validate_manifests()
