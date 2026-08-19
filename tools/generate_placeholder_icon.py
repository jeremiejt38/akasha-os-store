#!/usr/bin/env python3
"""Generate a simple 256x256 placeholder icon for an app."""
import argparse
import hashlib
import os
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


def color_from_id(app_id: str) -> tuple[int, int, int]:
    """Deterministic color from the app id."""
    digest = hashlib.sha256(app_id.encode()).hexdigest()
    return int(digest[:2], 16), int(digest[2:4], 16), int(digest[4:6], 16)


def generate_icon(app_id: str, output_path: Path):
    size = 256
    img = Image.new("RGBA", (size, size), (15, 17, 23, 255))
    draw = ImageDraw.Draw(img)
    color = color_from_id(app_id)
    # Draw a circle with the app color
    margin = 32
    draw.ellipse([margin, margin, size - margin, size - margin], fill=(*color, 255))

    # Centered initials
    initials = "".join(part[0].upper() for part in app_id.split(".")[-2:])[:2]
    if not initials:
        initials = app_id[:2].upper()

    font_size = 96
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)
    except OSError:
        font = ImageFont.load_default()

    bbox = draw.textbbox((0, 0), initials, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = (size - text_width) / 2
    y = (size - text_height) / 2 - 8
    draw.text((x, y), initials, fill=(255, 255, 255, 255), font=font)

    img.save(output_path, "PNG", optimize=True)
    print(f"Generated {output_path} ({os.path.getsize(output_path)} bytes)")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("app_id")
    parser.add_argument("-o", "--output", type=Path, default=None)
    args = parser.parse_args()
    output = args.output or Path(f"apps/{args.app_id}/icon.png")
    output.parent.mkdir(parents=True, exist_ok=True)
    generate_icon(args.app_id, output)
