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

# install.type values whose source_url is *only* an informative "learn more"
# link shown to the user, never actually fetched by the real install flow
# (that's exactly what distinguishes them from kodi-repo/zip-url, whose
# source_url the Store module really does need to download from). A CI
# runner's datacenter IP gets blocked by commercial anti-bot protection
# (Akamai/Cloudflare, IP reputation) far more aggressively and
# unpredictably than a home connection -- confirmed live: the exact same
# manifests that passed locally failed in Actions with different domains
# 403/406-ing each run, entirely unrelated to whether the site is actually
# up. Failing CI on that noise would block unrelated PRs indefinitely, so
# these types only get a printed warning, never a hard failure.
ADVISORY_ONLY_INSTALL_TYPES = {"external-app", "script"}


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
        #
        # For external-app/script, a failure here is only ever printed as a
        # warning (see ADVISORY_ONLY_INSTALL_TYPES above) -- these
        # source_urls are informative-only, and CI datacenter IPs get
        # blocked by this exact class of anti-bot protection far more
        # unpredictably than the actual liveness of the linked site.
        install_type = manifest["install"]["type"]
        source_url = manifest["install"]["source_url"]
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
                message = f"{app_dir.name}: source_url returned {resp.status_code}"
                if install_type in ADVISORY_ONLY_INSTALL_TYPES:
                    print(f"warning: {message}", file=sys.stderr)
                else:
                    errors.append(message)
                    continue
        except requests.RequestException as exc:
            message = f"{app_dir.name}: source_url unreachable ({exc})"
            if install_type in ADVISORY_ONLY_INSTALL_TYPES:
                print(f"warning: {message}", file=sys.stderr)
            else:
                errors.append(message)
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
