#!/usr/bin/env python3
"""Generate ``apps/<id>/manifest.json`` files from ``tools/apps_seed.py``.

Usage:  python tools/seed_apps.py
Idempotent: skips manifests that already exist (safe to re-run).
Icons are fetched separately by ``tools/fetch_icons.py`` — a placeholder
letter icon is created for new apps so the entry is valid immediately.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'tools'))
from apps_seed import APPS  # noqa: E402
from generate_placeholder_icon import generate_icon  # noqa: E402

TODAY = '2026-11-03'


def manifest_for(app):
    data = {
        'id': app['id'],
        'name': app['name'],
        'version': '1.0.0',
        'category': app['category'],
        'description': app['description'],
        'icon': 'icon.png',
        'install': app['install'],
        'legal_notice': app['legal'],
        'min_os_version': '12.0',
        'maintainer': 'jeremiejt38',
        'last_verified': TODAY,
    }
    if app.get('deep_link'):
        data['deep_link'] = app['deep_link']
    return data


def main():
    created, skipped = 0, 0
    for app in APPS:
        app_dir = ROOT / 'apps' / app['id']
        manifest_path = app_dir / 'manifest.json'
        icon_path = app_dir / 'icon.png'
        if manifest_path.exists():
            skipped += 1
            continue
        app_dir.mkdir(parents=True, exist_ok=True)
        manifest_path.write_text(
            json.dumps(manifest_for(app), indent=2, ensure_ascii=False) + '\n',
            encoding='utf-8')
        if not icon_path.exists():
            generate_icon(app['id'], icon_path)
        created += 1
    print(f'{created} manifests created, {skipped} already existed')


if __name__ == '__main__':
    main()
