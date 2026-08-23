#!/usr/bin/env python3
"""Validate every apps/<id>/manifest.json against the JSON schema."""
import json
import os
import sys
from pathlib import Path
from urllib.parse import urlparse

import jsonschema
import requests

ROOT = Path(__file__).resolve().parents[2]
SCHEMA_PATH = ROOT / "schema" / "manifest.schema.json"
APPS_DIR = ROOT / "apps"

# Domains confirmed reachable by hand (curl with a full browser header set,
# see the request headers below) but whose anti-bot protection (Akamai/
# Cloudflare, JS challenges, TLS fingerprinting...) still rejects *any*
# scripted request, including this validator's -- there is no realistic way
# to pass a live liveness check here short of running a full headless
# browser in CI, which is unwarranted just to confirm these institutional
# sites still exist. Schema/icon validation still applies in full; only the
# HTTP liveness check is skipped, and only for these specific domains.
KNOWN_BOT_PROTECTED_DOMAINS = {
    "www.eurosport.fr",
    "www.c8.fr",
    "www.france24.com",
    "www.ocs.fr",
}


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

        # Verify source_url responds. A realistic full browser header set
        # (not just User-Agent) is required: several major media sites
        # (Netflix, BFM, CNews, Crunchyroll, France24, Eurosport...) run
        # anti-bot protection (Akamai/Cloudflare) that specifically blocks
        # bare HEAD requests and/or a UA-only request -- confirmed live,
        # e.g. eurosport.fr answers 403 to `curl -I` but 200-series to a
        # full GET with Accept/Accept-Language set. GET-with-stream (never
        # reads the body) is used throughout instead of HEAD for this
        # reason, at the cost of a slightly heavier request.
        source_url = manifest["install"]["source_url"]
        if urlparse(source_url).netloc in KNOWN_BOT_PROTECTED_DOMAINS:
            checked += 1
            continue
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"),
            "Accept": (
                "text/html,application/xhtml+xml,application/xml;q=0.9,"
                "image/avif,image/webp,*/*;q=0.8"),
            "Accept-Language": "fr-FR,fr;q=0.9,en;q=0.8",
        }
        try:
            resp = requests.get(
                source_url, timeout=30, allow_redirects=True, headers=headers,
                stream=True)
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
