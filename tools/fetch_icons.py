#!/usr/bin/env python3
"""Fetch official app icons for the Akasha OS Store catalogue.

For each app id the script tries, in order:
  1. Google Play ``og:image`` of the app page (``play:<package>``)
  2. iTunes Search API ``artworkUrl512`` (``itunes:<term>``)
  3. SimpleIcons brand glyph rendered on a dark tile (``simple:<slug>``)
  4. Keep the existing ``icon.png`` untouched (letter avatar)

The downloaded artwork is normalized to a 256x256 PNG with rounded corners,
matching the Android TV / Play Store tile look, and kept under 100 KiB.

Usage:
    python tools/fetch_icons.py              # fetch all icons
    python tools/fetch_icons.py video.netflix # a single app
"""
import io
import json
import re
import sys
import urllib.parse
from pathlib import Path

import requests
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'tools'))
from apps_seed import APPS, EXISTING_ICONS  # noqa: E402

UA = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0'}
SIZE = 256
RADIUS = 56  # ~22% — Play Store squircle look
MAX_BYTES = 95 * 1024
TIMEOUT = 15

# Brand colours for SimpleIcons fallbacks (dark tile + tinted glyph).
SIMPLE_TILE = (24, 26, 32)


def fetch_play(package):
    """Return PIL image of the Play Store icon for an Android package id."""
    url = ('https://play.google.com/store/apps/details?id={}&hl=fr&gl=US'
           .format(urllib.parse.quote(package)))
    r = requests.get(url, headers=UA, timeout=TIMEOUT)
    if r.status_code != 200:
        return None
    m = re.search(r'<meta[^>]+property="og:image"[^>]+content="([^"]+)"', r.text)
    if not m:
        m = re.search(r'"(https://play-lh\.googleusercontent\.com/[^"\\]+)"', r.text)
    if not m:
        return None
    icon_url = re.sub(r'=.*$', '', m.group(1)) + '=s512-rw'
    r = requests.get(icon_url, headers=UA, timeout=TIMEOUT)
    if r.status_code != 200 or len(r.content) < 1024:
        return None
    return Image.open(io.BytesIO(r.content)).convert('RGBA')


def fetch_playsearch(term):
    """Search Google Play for an app name, then fetch its icon."""
    url = ('https://play.google.com/store/search?q={}&c=apps&hl=fr&gl=US'
           .format(urllib.parse.quote(term)))
    r = requests.get(url, headers=UA, timeout=TIMEOUT)
    if r.status_code != 200:
        return None
    m = re.search(r'/store/apps/details\?id=([A-Za-z0-9._]+)', r.text)
    if not m:
        return None
    return fetch_play(m.group(1))


ITUNES_COUNTRIES = ['fr', 'us', 'gb', 'de', 'it', 'es', 'se', 'no', 'be', 'ch', 'nl']


def fetch_itunes(term):
    """Return PIL image of the first App Store artworkUrl512 match.

    Apps are often regional (ITVX only exists on the UK store, RaiPlay on the
    Italian one...), so several storefronts are tried until a match is found.
    """
    for country in ITUNES_COUNTRIES:
        try:
            r = requests.get('https://itunes.apple.com/search', params={
                'term': term, 'entity': 'software',
                'country': country, 'limit': 3,
            }, headers=UA, timeout=TIMEOUT)
            if r.status_code != 200:
                continue
            if r.status_code == 429:
                print('   itunes rate-limited, skipping remaining countries')
                return None
            for result in r.json().get('results', []):
                artwork = result.get('artworkUrl512')
                if not artwork:
                    continue
                ir = requests.get(artwork, headers=UA, timeout=TIMEOUT)
                if ir.status_code == 200 and len(ir.content) > 2048:
                    try:
                        return Image.open(io.BytesIO(ir.content)).convert('RGBA')
                    except Exception:
                        continue
        except Exception:
            continue
    return None


def fetch_simple(slug):
    """Render a SimpleIcons glyph on a dark tile."""
    r = requests.get('https://cdn.simpleicons.org/{}/FFFFFF'.format(slug),
                     headers=UA, timeout=TIMEOUT)
    if r.status_code != 200 or b'<svg' not in r.content[:2048]:
        return None
    svg = ROOT / '_tmp_icon.svg'
    png = ROOT / '_tmp_icon.png'
    try:
        svg.write_bytes(r.content)
        import subprocess
        proc = subprocess.run(
            ['convert', '-background', 'none', '-density', '300',
             str(svg), '-resize', '160x160', str(png)],
            capture_output=True, timeout=TIMEOUT)
        if proc.returncode != 0 or not png.exists():
            return None
        glyph = Image.open(png).convert('RGBA')
        tile = Image.new('RGBA', (SIZE, SIZE), SIMPLE_TILE + (255,))
        tile.paste(glyph, ((SIZE - glyph.width) // 2,
                           (SIZE - glyph.height) // 2), glyph)
        return tile
    except Exception:
        return None
    finally:
        svg.unlink(missing_ok=True)
        png.unlink(missing_ok=True)


def normalize(img):
    """Resize to 256x256 and apply the rounded-corner mask."""
    img = img.convert('RGBA')
    # Letterbox onto a square if the source is not square.
    if img.width != img.height:
        side = max(img.width, img.height)
        canvas = Image.new('RGBA', (side, side), (0, 0, 0, 0))
        canvas.paste(img, ((side - img.width) // 2,
                           (side - img.height) // 2), img)
        img = canvas
    img = img.resize((SIZE, SIZE), Image.LANCZOS)
    mask = Image.new('L', (SIZE, SIZE), 0)
    ImageDraw.Draw(mask).rounded_rectangle(
        [0, 0, SIZE - 1, SIZE - 1], radius=RADIUS, fill=255)
    img.putalpha(Image.composite(img.getchannel('A'), Image.new('L', (SIZE, SIZE), 0), mask))
    return img


def save_png(img, path):
    """Save under MAX_BYTES, downscaling if needed."""
    buf = io.BytesIO()
    img.save(buf, 'PNG', optimize=True)
    if buf.tell() <= MAX_BYTES:
        path.write_bytes(buf.getvalue())
        return
    # Quantize to a palette (keeps alpha) if still too large.
    q = img.quantize(colors=255, method=Image.FASTOCTREE)
    buf = io.BytesIO()
    q.save(buf, 'PNG', optimize=True)
    if buf.tell() <= MAX_BYTES:
        path.write_bytes(buf.getvalue())
        return
    small = img.resize((192, 192), Image.LANCZOS)
    buf = io.BytesIO()
    small.save(buf, 'PNG', optimize=True)
    path.write_bytes(buf.getvalue())


def fetch_one(app_id, hints):
    """Try all hints in order; return the first usable image."""
    for kind, value in hints:
        try:
            if kind == 'play':
                img = fetch_play(value)
            elif kind == 'playsearch':
                img = fetch_playsearch(value)
            elif kind == 'itunes':
                img = fetch_itunes(value)
            elif kind == 'simple':
                img = fetch_simple(value)
            else:
                continue
            if img is not None:
                return img, '{}:{}'.format(kind, value)
        except Exception:
            continue
    return None, None


def main():
    only = sys.argv[1] if len(sys.argv) > 1 else None
    hints = dict(EXISTING_ICONS)
    for app in APPS:
        hints[app['id']] = app['icons']

    ok, missing = 0, []
    for app_id in sorted(hints):
        if only and app_id != only:
            continue
        icon_path = ROOT / 'apps' / app_id / 'icon.png'
        if not icon_path.parent.exists():
            print('SKIP {} (no app dir)'.format(app_id))
            continue
        app_hints = list(hints[app_id])
        try:
            name = json.loads(
                (icon_path.parent / 'manifest.json').read_text())['name']
            clean = re.sub(r'\s*\(.*?\)\s*', '', name).strip()
            app_hints.append(('playsearch', clean))
            app_hints.append(('itunes', clean))
        except Exception:
            pass
        img, src = fetch_one(app_id, app_hints)
        if img is None:
            missing.append(app_id)
            print('MISS {}'.format(app_id))
            continue
        save_png(normalize(img), icon_path)
        ok += 1
        print('OK   {} <- {}'.format(app_id, src))
    print('---\n{} icons fetched, {} missing'.format(ok, len(missing)))
    if missing:
        print('missing:', ', '.join(missing))


if __name__ == '__main__':
    main()
