#!/usr/bin/env python3
"""Make one PNG per graph that the outline asks for, using the brand colors.

Run from the workspace root:
    python3 03_graphs/_tools/make_graphs.py

Dependencies: matplotlib (python3 -m pip install matplotlib).
Everything else is the standard library.

Which graphs are made: only slides in 02_Processing/output/outline.md whose
"- Graph:" line is not "none". The line has the form
    - Graph: <question the graph answers> | data: <file.csv>
The question becomes the chart title. CSV files that no slide asks for are
not plotted. If a named file is missing from input/, that graph is skipped.

CSV format: header row; first column = category labels, second column =
numbers. Put the unit in the header, e.g. "Satisfaction (score 1-5)".
Comma or semicolon separators are accepted; a decimal comma is read as a
decimal point.
"""
import csv
import re
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

# Paths are resolved from this file's location, so folder-name casing on disk
# (03_Graphs vs 03_graphs, Constraints vs constraints) does not matter.
STAGE = Path(__file__).resolve().parent.parent
ROOT = STAGE.parent
IN_DIR = STAGE / "input"
OUT_DIR = STAGE / "output" / "graphs"
OUTLINE = ROOT / "02_Processing" / "output" / "outline.md"
FALLBACK_COLOR = "#7f7f7f"
HEX = re.compile(r"#[0-9A-Fa-f]{6}\b")


def find_ci(parent: Path, name: str) -> Path:
    """Child of parent matching name case-insensitively (else parent/name)."""
    if parent.is_dir():
        for child in parent.iterdir():
            if child.name.lower() == name.lower():
                return child
    return parent / name


BRAND = find_ci(find_ci(ROOT, "constraints"), "brand.md")


def brand_colors() -> list[str]:
    """Hex codes from the 'Colors' section of brand.md, primary first."""
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


def requested_graphs() -> list[tuple[str, str, str]]:
    """(slide, question, data file) for every Graph line that is not 'none'."""
    if not OUTLINE.is_file():
        print(f"note: {OUTLINE} not found, no graphs requested")
        return []
    out, slide = [], "?"
    for line in OUTLINE.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^##\s+(Slide\s+\d+)", line)
        if m:
            slide = m.group(1)
            continue
        m = re.match(r"^- Graph:\s*(.+?)\s*$", line)
        if not m or m.group(1).lower() == "none":
            continue
        g = re.match(r"^(.+?)\s*\|\s*data:\s*(\S+)", m.group(1))
        if g:
            out.append((slide, g.group(1), g.group(2)))
        else:
            print(f"note: {slide} Graph line names no data file, skipped")
    return out


def read_rows(path: Path) -> list[list[str]]:
    with path.open(newline="", encoding="utf-8") as fh:
        dialect = csv.Sniffer().sniff(fh.read(4096), delimiters=",;")
        fh.seek(0)
        return [row for row in csv.reader(fh, dialect) if any(c.strip() for c in row)]


def make_chart(slide: str, path: Path, color: str, title: str) -> bool:
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
    ax.set_title(title, loc="left", fontsize=13)
    ax.set_xlabel(header[0])
    ax.set_ylabel(header[1])
    ax.spines[["top", "right"]].set_visible(False)
    fig.text(0.01, 0.01, f"Source: 03_graphs/input/{path.name}", fontsize=8, color="#555555")
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    slug = slide.lower().replace(" ", "")
    out = OUT_DIR / f"{slug}_{path.stem}.png"
    fig.savefig(out)
    plt.close(fig)
    print(f"wrote {out.relative_to(ROOT)}")
    return True


def main() -> int:
    wanted = requested_graphs()
    if not wanted:
        print("The outline asks for no graphs (every Graph line is 'none'). Nothing to do.")
        return 0
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    color = brand_colors()[0]
    made = 0
    for slide, question, data in wanted:
        path = IN_DIR / data
        if not path.is_file():
            print(f"SKIP {slide}: {data} not found in input/")
            continue
        made += make_chart(slide, path, color, question)
    print(f"{made} of {len(wanted)} graph(s) written.")
    return 0 if made == len(wanted) else 1


if __name__ == "__main__":
    sys.exit(main())
