#!/usr/bin/env python3
"""Make one PNG per CSV in 03_graphs/input/, using the brand colors.

Run from the workspace root:
    python3 03_graphs/_tools/make_graphs.py

Dependencies: matplotlib (python3 -m pip install matplotlib).
Everything else is the standard library.

Input: each CSV has a header row. The first column gives the category
labels, the second column gives the numbers. Put the unit in the header,
for example "Satisfaction (score 1-5)". Comma or semicolon separators
are both accepted, and a decimal comma is read as a decimal point.
"""
import csv
import re
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

ROOT = Path.cwd()
IN_DIR = ROOT / "03_graphs" / "input"
OUT_DIR = ROOT / "03_graphs" / "output" / "graphs"
BRAND = ROOT / "constraints" / "brand.md"
FALLBACK_COLOR = "#7f7f7f"
HEX = re.compile(r"#[0-9A-Fa-f]{6}\b")


def brand_colors() -> list[str]:
    """Hex codes from the 'Colors' table in brand.md, primary first."""
    if not BRAND.is_file():
        print(f"note: {BRAND} not found, using gray")
        return [FALLBACK_COLOR]
    colors, in_colors = [], False
    for line in BRAND.read_text(encoding="utf-8").splitlines():
        if line.startswith("## "):
            in_colors = line.strip() == "## Colors"
        elif in_colors:
            colors += HEX.findall(line)
    if not colors:
        print("note: no hex colors in brand.md 'Colors' section, using gray")
        return [FALLBACK_COLOR]
    return colors


def read_rows(path: Path) -> list[list[str]]:
    with path.open(newline="", encoding="utf-8") as fh:
        dialect = csv.Sniffer().sniff(fh.read(4096), delimiters=",;")
        fh.seek(0)
        return [row for row in csv.reader(fh, dialect) if any(cell.strip() for cell in row)]


def make_chart(path: Path, color: str) -> bool:
    rows = read_rows(path)
    header, body = rows[0], rows[1:]
    labels = [row[0] for row in body]
    try:
        values = [float(row[1].replace(",", ".")) for row in body]
    except (ValueError, IndexError) as err:
        print(f"SKIP {path.name}: second column is not numeric ({err})")
        return False

    fig, ax = plt.subplots(figsize=(8, 4.5), dpi=150)
    ax.bar(labels, values, color=color)
    ax.set_title(path.stem.replace("_", " "), loc="left", fontsize=13)
    ax.set_xlabel(header[0])
    ax.set_ylabel(header[1])
    ax.spines[["top", "right"]].set_visible(False)
    fig.text(0.01, 0.01, f"Source: 03_graphs/input/{path.name}", fontsize=8, color="#555555")
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    out = OUT_DIR / f"{path.stem}.png"
    fig.savefig(out)
    plt.close(fig)
    print(f"wrote {out.relative_to(ROOT)}")
    return True


def main() -> int:
    csv_files = sorted(IN_DIR.glob("*.csv"))
    if not csv_files:
        print("No CSV files in 03_graphs/input/. Nothing to do.")
        return 0
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    colors = brand_colors()
    made = sum(make_chart(p, colors[0]) for p in csv_files)
    print(f"{made} of {len(csv_files)} graph(s) written.")
    return 0 if made == len(csv_files) else 1


if __name__ == "__main__":
    sys.exit(main())
