#!/usr/bin/env python3
"""Render contact sheets for one or more PDF files.

Useful for page-by-page visual QA of long Google Docs preview exports.
Uses PyMuPDF when installed, otherwise falls back to pdftoppm + Pillow.

Example:
  python render_pdf_contact_sheets.py \
    --inputs /tmp/requirements.pdf /tmp/architecture.pdf \
    --out-dir /tmp/page_audit_sheets
"""

from __future__ import annotations

import argparse
import math
import shutil
import subprocess
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageOps

try:
    import fitz
except ModuleNotFoundError:  # pragma: no cover - exercised only when PyMuPDF is absent
    fitz = None


def parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser()
    ap.add_argument("--inputs", nargs="+", required=True, help="PDF paths to render")
    ap.add_argument("--out-dir", required=True, help="Directory for generated contact sheets")
    ap.add_argument("--cols", type=int, default=2, help="Pages per row")
    ap.add_argument("--rows", type=int, default=4, help="Rows per sheet")
    ap.add_argument("--zoom", type=float, default=0.85, help="PDF render zoom scale")
    ap.add_argument("--margin", type=int, default=24, help="Outer and inter-tile margin")
    ap.add_argument("--label-height", type=int, default=28, help="Label height above each page")
    return ap.parse_args()


def render_contact_sheets(
    pdf_path: Path,
    out_dir: Path,
    cols: int,
    rows: int,
    zoom: float,
    margin: int,
    label_height: int,
) -> list[str]:
    pages_per_sheet = cols * rows
    label = pdf_path.stem.replace("_preview_latest", "")
    thumbs = render_pages(pdf_path, zoom)

    index_lines: list[str] = []
    for sheet_idx in range(math.ceil(len(thumbs) / pages_per_sheet)):
        chunk = thumbs[sheet_idx * pages_per_sheet : (sheet_idx + 1) * pages_per_sheet]
        tile_w = max(im.width for _, im in chunk)
        tile_h = max(im.height for _, im in chunk)
        sheet_w = cols * tile_w + (cols + 1) * margin
        sheet_h = rows * (tile_h + label_height) + (rows + 1) * margin

        sheet = Image.new("RGB", (sheet_w, sheet_h), "white")
        draw = ImageDraw.Draw(sheet)

        for idx, (page_no, im) in enumerate(chunk):
            r = idx // cols
            c = idx % cols
            x = margin + c * (tile_w + margin)
            y = margin + r * (tile_h + label_height + margin)
            draw.text((x, y), f"{label} p.{page_no}", fill="black")
            sheet.paste(im, (x, y + label_height))

        out_path = out_dir / f"{label}_sheet_{sheet_idx + 1:02d}.png"
        sheet.save(out_path, optimize=True)
        first = chunk[0][0]
        last = chunk[-1][0]
        index_lines.append(f"{out_path.name}: {label} pages {first}-{last}")

    return index_lines


def render_pages(pdf_path: Path, zoom: float) -> list[tuple[int, Image.Image]]:
    if fitz is not None:
        return render_pages_with_fitz(pdf_path, zoom)
    return render_pages_with_pdftoppm(pdf_path, zoom)


def render_pages_with_fitz(pdf_path: Path, zoom: float) -> list[tuple[int, Image.Image]]:
    doc = fitz.open(pdf_path)
    thumbs = []
    for i in range(doc.page_count):
        page = doc.load_page(i)
        pix = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom), alpha=False)
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        thumbs.append((i + 1, ImageOps.expand(img, border=2, fill="#c9c9c9")))
    return thumbs


def render_pages_with_pdftoppm(pdf_path: Path, zoom: float) -> list[tuple[int, Image.Image]]:
    if shutil.which("pdftoppm") is None:
        raise RuntimeError("PyMuPDF is not installed and pdftoppm is not available on PATH")

    dpi = max(36, int(72 * zoom))
    with tempfile.TemporaryDirectory() as tmp:
        prefix = Path(tmp) / "page"
        subprocess.run(
            ["pdftoppm", "-r", str(dpi), "-png", str(pdf_path), str(prefix)],
            check=True,
            capture_output=True,
            text=True,
        )
        page_paths = sorted(Path(tmp).glob("page-*.png"), key=lambda p: int(p.stem.split("-")[-1]))
        thumbs = []
        for i, path in enumerate(page_paths, start=1):
            img = Image.open(path).convert("RGB")
            img.load()
            thumbs.append((i, ImageOps.expand(img, border=2, fill="#c9c9c9")))
        return thumbs


def main() -> None:
    args = parse_args()
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    for existing in out_dir.glob("*.png"):
        existing.unlink()

    all_index: list[str] = []
    for raw_path in args.inputs:
        pdf_path = Path(raw_path)
        if not pdf_path.exists():
            raise FileNotFoundError(pdf_path)
        all_index.extend(
            render_contact_sheets(
                pdf_path=pdf_path,
                out_dir=out_dir,
                cols=args.cols,
                rows=args.rows,
                zoom=args.zoom,
                margin=args.margin,
                label_height=args.label_height,
            )
        )

    index_path = out_dir / "index.txt"
    index_path.write_text("\n".join(all_index) + "\n", encoding="utf-8")
    print(f"Rendered {len(all_index)} contact sheets to {out_dir}")


if __name__ == "__main__":
    main()
