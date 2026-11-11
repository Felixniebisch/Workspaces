#!/usr/bin/env python3
"""Build the presentation from the outline, using the brand rules and graphs.

Run from the workspace root:
    python3 04_Powerpoint/_tools/build_deck.py

Reads:
    02_Processing/output/outline.md   (fixed "## Slide N" format)
    constraints/brand.md              (Colors table, Fonts section)
    03_graphs/output/graphs/<name>.png (named after the data file in the Graph line)
Writes:
    04_Powerpoint/output/presentation.pptx

Dependencies: python-pptx (python3 -m pip install python-pptx).
Standard library otherwise.

A slide whose Graph line names a PNG that does not exist gets a visible
"GRAPH MISSING" box. Nothing is invented to fill a gap.
"""
import re
import sys
from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.util import Inches, Pt

ROOT = Path.cwd()
OUTLINE = ROOT / "02_Processing" / "output" / "outline.md"
BRAND = ROOT / "constraints" / "brand.md"
GRAPHS = ROOT / "03_graphs" / "output" / "graphs"
OUT = ROOT / "04_Powerpoint" / "output" / "presentation.pptx"

SLIDE_RE = re.compile(r"^## Slide (\d+)\s*$")
FIELD_RE = re.compile(r"^- (Title|Message|Sources|Graph|Open questions):\s*(.*)$")
HEX = re.compile(r"#([0-9A-Fa-f]{6})\b")
DEFAULT_FONT = "Calibri"
DEFAULT_COLOR = "1F4E79"


def parse_outline(text: str) -> tuple[list[dict], list[str]]:
    """Return (slides, open questions listed in the outline's own section)."""
    slides, cur, section, open_items = [], None, "", []
    for line in text.splitlines():
        if line.startswith("## "):
            section = line[3:].strip()
        if section == "Open questions" and line.startswith("- "):
            item = line[2:].strip()
            if item.lower() != "none":
                open_items.append(item)
            continue
        m = SLIDE_RE.match(line)
        if m:
            cur = {"number": int(m.group(1))}
            slides.append(cur)
            continue
        if cur is not None:
            f = FIELD_RE.match(line)
            if f:
                cur[f.group(1)] = f.group(2).strip()
    return slides, open_items


def brand_style() -> tuple[str, str, str]:
    """(heading font, body font, primary hex) from brand.md; defaults if TODO or missing."""
    if not BRAND.is_file():
        print("note: constraints/brand.md not found, using defaults")
        return DEFAULT_FONT, DEFAULT_FONT, DEFAULT_COLOR
    text = BRAND.read_text(encoding="utf-8")

    def value(label: str) -> str:
        m = re.search(rf"\*\*{label}:\*\*\s*(.+)", text)
        v = m.group(1).strip() if m else ""
        return "" if v.upper().startswith("TODO") or not v else v

    colors_section = re.search(r"^## Colors\s*$(.*?)(?=^## |\Z)", text, re.M | re.S)
    hexes = HEX.findall(colors_section.group(1)) if colors_section else []
    primary = hexes[0] if hexes else DEFAULT_COLOR
    heading = value("Headings") or DEFAULT_FONT
    body = value("Body") or DEFAULT_FONT
    if not hexes:
        print("note: no colors in brand.md, using default")
    return heading, body, primary


def rgb(hex6: str) -> RGBColor:
    return RGBColor.from_string(hex6.upper())


def add_text(slide, left, top, width, height, text, size, font, color, bold=False):
    box = slide.shapes.add_textbox(left, top, width, height)
    frame = box.text_frame
    frame.word_wrap = True
    para = frame.paragraphs[0]
    para.text = text
    para.font.size = Pt(size)
    para.font.name = font
    para.font.bold = bold
    para.font.color.rgb = rgb(color)
    return box


def build() -> int:
    if not OUTLINE.is_file():
        print(f"ERROR: {OUTLINE.relative_to(ROOT)} not found. Run the processing stage first.")
        return 1
    slides, outline_open = parse_outline(OUTLINE.read_text(encoding="utf-8"))
    if not slides:
        print("ERROR: no '## Slide N' entries found in the outline.")
        return 1

    heading_font, body_font, primary = brand_style()
    prs = Presentation()
    prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)
    layout = prs.slide_layouts[5]  # Title Only
    all_open, missing = list(outline_open), []

    for s in slides:
        n = s["number"]
        slide = prs.slides.add_slide(layout)
        title = slide.shapes.title
        title.left, title.top, title.width, title.height = Inches(0.6), Inches(0.4), Inches(12.1), Inches(1.1)
        title.text = s.get("Title", f"Slide {n}")
        for para in title.text_frame.paragraphs:
            para.font.name = heading_font
            para.font.size = Pt(34)
            para.font.bold = True
            para.font.color.rgb = rgb(primary)

        add_text(slide, Inches(0.6), Inches(1.7), Inches(5.6), Inches(4.8),
                 s.get("Message", ""), 22, body_font, "222222")

        graph = s.get("Graph", "none")
        if graph.lower() != "none":
            question, _, data_part = graph.partition("| data:")
            png = GRAPHS / (Path(data_part.strip()).stem + ".png")
            if png.is_file():
                slide.shapes.add_picture(str(png), Inches(6.6), Inches(1.8), width=Inches(6.1))
            else:
                box = slide.shapes.add_shape(1, Inches(6.6), Inches(1.8), Inches(6.1), Inches(4.2))
                box.fill.solid()
                box.fill.fore_color.rgb = rgb("F2F2F2")
                box.line.color.rgb = rgb("C00000")
                box.text_frame.text = f"GRAPH MISSING: {question.strip()}"
                box.text_frame.paragraphs[0].font.color.rgb = rgb("C00000")
                box.text_frame.paragraphs[0].font.size = Pt(18)
                missing.append(f"Slide {n}: graph '{question.strip()}' (expected {png.name})")

        notes = [f"Sources: {s.get('Sources', 'not given')}"]
        affecting = s.get("Open questions", "none")
        if affecting.lower() != "none":
            notes.append(f"Open questions: {affecting}")
            all_open.append(f"Slide {n}: {affecting}")
        slide.notes_slide.notes_text_frame.text = "\n".join(notes)

    if all_open:
        slide = prs.slides.add_slide(layout)
        slide.shapes.title.text = "Open items"
        add_text(slide, Inches(0.6), Inches(1.7), Inches(12.1), Inches(5.0),
                 "\n".join(f"- {item}" for item in all_open), 18, body_font, "222222")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    prs.save(OUT)
    print(f"wrote {OUT.relative_to(ROOT)} with {len(slides)} slide(s)"
          f"{' + open items slide' if all_open else ''}")
    for item in missing:
        print(f"WARNING {item}")
    return 0


if __name__ == "__main__":
    sys.exit(build())
