#!/usr/bin/env python3

from __future__ import annotations

import argparse
import shutil
import subprocess
import tempfile
from pathlib import Path

from PIL import Image


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Render local HTML diagrams to tightly cropped PNGs.")
    parser.add_argument(
        "--pair",
        action="append",
        required=True,
        help="Render pair in the form /abs/src.html::/abs/out.png",
    )
    parser.add_argument("--window-width", type=int, default=1800)
    parser.add_argument("--window-height", type=int, default=1400)
    parser.add_argument("--scale", type=float, default=2.0)
    parser.add_argument("--crop-pad", type=int, default=6)
    parser.add_argument("--timeout-ms", type=int, default=2500)
    return parser.parse_args()


def find_chrome() -> str:
    for candidate in ["google-chrome", "google-chrome-stable", "chromium", "chromium-browser"]:
        path = shutil.which(candidate)
        if path:
            return path
    raise SystemExit("No Chrome/Chromium binary found")


def crop_white_border(src: Path, dest: Path, crop_pad: int) -> None:
    with Image.open(src).convert("RGBA") as im:
        bg = Image.new("RGBA", im.size, (255, 255, 255, 255))
        flat = Image.alpha_composite(bg, im).convert("RGB")
        w, h = flat.size
        px = flat.load()
        left = w
        top = h
        right = -1
        bottom = -1

        for y in range(h):
            for x in range(w):
                r, g, b = px[x, y]
                if not (r >= 250 and g >= 250 and b >= 250):
                    left = min(left, x)
                    top = min(top, y)
                    right = max(right, x)
                    bottom = max(bottom, y)

        if right == -1:
            raise SystemExit(f"Rendered image appears blank: {src}")

        left = max(0, left - crop_pad)
        top = max(0, top - crop_pad)
        right = min(w, right + 1 + crop_pad)
        bottom = min(h, bottom + 1 + crop_pad)

        cropped = flat.crop((left, top, right, bottom))
        dest.parent.mkdir(parents=True, exist_ok=True)
        cropped.save(dest, format="PNG", optimize=True)


def render_pair(chrome: str, src_html: Path, dest_png: Path, window_w: int, window_h: int, scale: float, timeout_ms: int, crop_pad: int) -> None:
    if not src_html.exists():
        raise SystemExit(f"Missing HTML source: {src_html}")

    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
        tmp_path = Path(tmp.name)

    try:
        cmd = [
            chrome,
            "--headless=new",
            "--disable-gpu",
            "--hide-scrollbars",
            f"--force-device-scale-factor={scale}",
            f"--window-size={window_w},{window_h}",
            f"--virtual-time-budget={timeout_ms}",
            "--run-all-compositor-stages-before-draw",
            f"--screenshot={tmp_path}",
            src_html.resolve().as_uri(),
        ]
        subprocess.run(cmd, check=True, capture_output=True, text=True)
        crop_white_border(tmp_path, dest_png, crop_pad)
    finally:
        tmp_path.unlink(missing_ok=True)


def main() -> None:
    args = parse_args()
    chrome = find_chrome()
    for pair in args.pair:
        src_raw, dest_raw = pair.split("::", 1)
        render_pair(
            chrome=chrome,
            src_html=Path(src_raw),
            dest_png=Path(dest_raw),
            window_w=args.window_width,
            window_h=args.window_height,
            scale=args.scale,
            timeout_ms=args.timeout_ms,
            crop_pad=args.crop_pad,
        )
        print(f"Rendered {src_raw} -> {dest_raw}")


if __name__ == "__main__":
    main()
