"""Rasterize an SVG to PNG using Playwright (headless Chromium).

Usage:
    python export_png.py                           # default: y-compact SVG
    python export_png.py some-diagram.svg          # custom input
    python export_png.py some-diagram.svg out.png  # custom input + output
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

# =========================
# Settings (edit defaults)
# =========================
HERE = Path(__file__).resolve().parent
DEFAULT_SVG = HERE / "diagram-1-option-c-process-rail_fixed_JVDB_y-compact.svg"


def read_svg_dimensions(svg_path: Path) -> tuple[int, int]:
    head = svg_path.read_text(encoding="utf-8")[:1000]
    wm = re.search(r'\bwidth="(\d+)"', head)
    hm = re.search(r'\bheight="(\d+)"', head)
    if not wm or not hm:
        raise ValueError(f"Could not parse width/height from {svg_path.name}")
    return int(wm.group(1)), int(hm.group(1))


def export_svg_to_png(svg_path: Path, png_path: Path) -> None:
    from playwright.sync_api import sync_playwright

    w, h = read_svg_dimensions(svg_path)
    url = svg_path.resolve().as_uri()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": w, "height": h})
        page.goto(url, wait_until="networkidle", timeout=15000)
        page.wait_for_timeout(2000)
        page.screenshot(
            path=str(png_path),
            clip={"x": 0, "y": 0, "width": w, "height": h},
            timeout=10000,
        )
        browser.close()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "svg", nargs="?", type=Path, default=DEFAULT_SVG,
        help=f"Input SVG (default: {DEFAULT_SVG.name})",
    )
    parser.add_argument(
        "png", nargs="?", type=Path, default=None,
        help="Output PNG (default: same basename as SVG)",
    )
    args = parser.parse_args()
    svg: Path = args.svg.resolve() if args.svg.is_absolute() else (HERE / args.svg).resolve()
    if not svg.is_file():
        print(f"SVG not found: {svg}", file=sys.stderr)
        return 2
    png: Path = args.png if args.png else svg.with_suffix(".png")

    export_svg_to_png(svg, png)
    print(f"Wrote {png}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
