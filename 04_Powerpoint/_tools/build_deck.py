#!/usr/bin/env python3
"""Build the presentation from the outline, using the brand rules and graphs.

Run from the workspace root:
    python3 04_Powerpoint/_tools/build_deck.py

Reads:
    02_Processing/output/outline.md    (fixed "## Slide N" format)
    constraints/brand.md               (brand name, Colors table, Fonts, Logo)
    03_graphs/output/graphs/<name>.png (named after the data file in the Graph line)
Writes:
    04_Powerpoint/output/presentation.pptx

Dependencies: python-pptx (python3 -m pip install python-pptx).
Standard library otherwise.

Layout (from brand.md "Layout style"): square corners only; near-white text
on the primary-color header band, near-black text on the light body; every
heading has a subheader (the outline's topic). Everything in the body section
below the header is centered horizontally and vertically: a message alone
sits in the middle; a message with a graph forms one centered block. The brand name is written in
6 pt in the accent color in the bottom-right corner (brand.md "Logo").

A slide whose Graph line names a PNG that does not exist gets a visible
"GRAPH MISSING" box. Nothing is invented to fill a gap. TODO brand fields
fall back to neutral defaults and are listed on the "Open items" slide.
"""
import re
import sys
from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches, Pt

ROOT = Path.cwd()
OUTLINE = ROOT / "02_Processing" / "output" / "outline.md"
BRAND = ROOT / "constraints" / "brand.md"
GRAPHS = ROOT / "03_graphs" / "output" / "graphs"
OUT = ROOT / "04_Powerpoint" / "output" / "presentation.pptx"

SLIDE_RE = re.compile(r"^## Slide (\d+)\s*$")
FIELD_RE = re.compile(r"^- (Title|Message|Sources|Graph|Open questions):\s*(.*)$")
HEX = re.compile(r"#([0-9A-Fa-f]{6})\b")
DEFAULTS = {"Primary": "404040", "Secondary": "7F7F7F", "Accent": "7F7F7F"}
DEFAULT_FONT = "Calibri"
NEAR_WHITE = "F7F5F0"
NEAR_BLACK = "1A1A1A"
OPEN_ITEMS_PER_SLIDE = 6

W, H = Inches(13.333), Inches(7.5)
MARGIN = Inches(0.6)
BAND_H = Inches(1.75)


# ---------- reading inputs ----------

def parse_outline(text: str) -> tuple[list[dict], list[str], str]:
    """Return (slides, open questions from the outline's own section, topic)."""
    slides, cur, section, open_items, topic = [], None, "", [], ""
    for line in text.splitlines():
        if line.startswith("## "):
            section = line[3:].strip()
        if section == "Goal and audience":
            m = re.match(r"^- \*\*Topic:\*\*\s*(.+?)\.?\s*$", line)
            if m:
                topic = m.group(1)
        if section == "Open questions":
            m = re.match(r"^(?:- |\d+\.\s+)(.+)$", line)
            if m:
                item = m.group(1).replace("**", "").replace("`", "").strip()
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
    return slides, open_items, topic


def section_text(text: str, name: str) -> str:
    m = re.search(rf"^## {re.escape(name)}\s*$(.*?)(?=^## |\Z)", text, re.M | re.S)
    return m.group(1).strip() if m else ""


def is_todo(value: str) -> bool:
    return not value or value.upper().startswith("TODO")


def brand_style() -> tuple[dict, list[str]]:
    """Brand values from brand.md, plus a list of fields that fell back to defaults."""
    gaps = []
    style = {"name": "", "heading": DEFAULT_FONT, "body": DEFAULT_FONT, "logo": False, **DEFAULTS}
    if not BRAND.is_file():
        return style, ["constraints/brand.md not found: default colors and fonts used"]
    text = BRAND.read_text(encoding="utf-8")

    name = section_text(text, "Brand name")
    if is_todo(name):
        gaps.append("Brand name is TODO in constraints/brand.md")
    else:
        style["name"] = name.splitlines()[0].strip()

    for row in section_text(text, "Colors").splitlines():
        cells = [c.strip() for c in row.strip("|").split("|")]
        if cells and cells[0] in DEFAULTS:
            m = HEX.search(row)
            if m:
                style[cells[0]] = m.group(1).upper()
            else:
                gaps.append(f"{cells[0]} color is TODO in constraints/brand.md: neutral gray used")

    for label, key in (("Headings", "heading"), ("Body", "body")):
        m = re.search(rf"\*\*{label}:\*\*\s*(.+)", text)
        v = m.group(1).strip() if m else ""
        if is_todo(v):
            gaps.append(f"{label} font is TODO in constraints/brand.md: {DEFAULT_FONT} used")
        else:
            style[key] = v

    logo = section_text(text, "Logo")
    if is_todo(logo):
        gaps.append("Logo is TODO in constraints/brand.md: no logo placed")
    else:
        style["logo"] = bool(style["name"])
    return style, gaps


# ---------- drawing helpers ----------

def rgb(hex6: str) -> RGBColor:
    return RGBColor.from_string(hex6.upper())


def rect(slide, left, top, width, height, fill):
    """Square-cornered filled rectangle without outline."""
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = rgb(fill)
    shape.line.fill.background()
    shape.shadow.inherit = False
    return shape


def add_text(slide, left, top, width, height, lines, size, font, color,
             bold=False, anchor=MSO_ANCHOR.TOP, align=PP_ALIGN.LEFT, space_after=0):
    box = slide.shapes.add_textbox(left, top, width, height)
    frame = box.text_frame
    frame.word_wrap = True
    frame.vertical_anchor = anchor
    frame.margin_left = frame.margin_right = 0
    for i, line in enumerate([lines] if isinstance(lines, str) else lines):
        para = frame.paragraphs[0] if i == 0 else frame.add_paragraph()
        para.text = line
        para.alignment = align
        para.space_after = Pt(space_after)
        para.font.size = Pt(size)
        para.font.name = font
        para.font.bold = bold
        para.font.color.rgb = rgb(color)
    return box


def base_slide(prs, style, title, subheader):
    """Blank slide with header band, title, subheader and logo."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])  # Blank
    rect(slide, 0, 0, W, BAND_H, style["Primary"])
    rect(slide, 0, BAND_H, W, Inches(0.06), style["Accent"])
    add_text(slide, MARGIN, Inches(0.3), W - 2 * MARGIN, Inches(0.85), title,
             32 if len(title) <= 45 else 26, style["heading"], NEAR_WHITE,
             anchor=MSO_ANCHOR.BOTTOM)
    add_text(slide, MARGIN, Inches(1.15), W - 2 * MARGIN, Inches(0.45), subheader,
             15, style["body"], NEAR_WHITE)
    if style["logo"]:
        add_text(slide, W - Inches(2.6), H - Inches(0.35), Inches(2.3), Inches(0.2),
                 style["name"], 6, style["body"], style["Accent"], align=PP_ALIGN.RIGHT)
    return slide


GRAPH_ASPECT = 8 / 4.5  # width / height of the PNGs from 03_graphs


def text_height(text: str, width, size: float) -> int:
    """Rough height (EMU) of wrapped text: ~0.5 em per character, 1.2 line spacing."""
    chars_per_line = max(1, int(width / 914400 * 72 / (size * 0.5)))
    lines = max(1, -(-len(text) // chars_per_line))
    return int(Pt(size * 1.2 * lines + 6))


def strip_known(question: str, known: list[str]) -> str:
    """Remove text already listed in the outline's open questions; return the rest."""
    rest = question
    for item in known:
        rest = rest.replace(item.rstrip(". "), "")
    return rest.strip(" ;.,") and rest


# ---------- build ----------

def build() -> int:
    if not OUTLINE.is_file():
        print(f"ERROR: {OUTLINE.relative_to(ROOT)} not found. Run the processing stage first.")
        return 1
    slides, outline_open, topic = parse_outline(OUTLINE.read_text(encoding="utf-8"))
    if not slides:
        print("ERROR: no '## Slide N' entries found in the outline.")
        return 1

    style, brand_gaps = brand_style()
    for gap in brand_gaps:
        print(f"note: {gap}")
    subheader = topic or "TODO: topic missing in outline"

    prs = Presentation()
    prs.slide_width, prs.slide_height = W, H
    all_open, missing = list(outline_open) + brand_gaps, []
    # Body section: everything below the header component, centered (brand.md "Layout style").
    body_top = BAND_H + Inches(0.06)
    body_bottom = H - Inches(0.45)  # keeps clear of the corner logo
    body_h = body_bottom - body_top
    text_w = W - 2 * MARGIN - Inches(1.0)
    text_left = (W - text_w) // 2

    for s in slides:
        n = s["number"]
        slide = base_slide(prs, style, s.get("Title", f"Slide {n}"), subheader)
        message = s.get("Message", "")

        graph = s.get("Graph", "none")
        has_graph = graph.lower() != "none"
        if not has_graph:
            # Message alone: centered in the middle of the body section.
            add_text(slide, text_left, body_top, text_w, body_h, message, 30,
                     style["body"], NEAR_BLACK, anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)

        if has_graph:
            # Message above graph; the pair is centered as one block in the body section.
            size, gap = 22, Inches(0.2)
            msg_h = text_height(message, text_w, size)
            graph_h = body_h - msg_h - gap - Inches(0.5)
            graph_w = min(int(graph_h * GRAPH_ASPECT), W - 2 * MARGIN)
            graph_h = int(graph_w / GRAPH_ASPECT)
            top = body_top + (body_h - (msg_h + gap + graph_h)) // 2
            add_text(slide, text_left, top, text_w, msg_h, message, size,
                     style["body"], NEAR_BLACK, anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)
            question, _, data_part = graph.partition("| data:")
            png = GRAPHS / (Path(data_part.strip()).stem + ".png")
            left, width, gtop = (W - graph_w) // 2, graph_w, top + msg_h + gap
            if png.is_file():
                slide.shapes.add_picture(str(png), left, gtop, width=width)
            else:
                box = rect(slide, left, gtop, width, graph_h, "F2F2F2")
                box.line.color.rgb = rgb("C00000")
                box.text_frame.text = f"GRAPH MISSING: {question.strip()}"
                box.text_frame.paragraphs[0].font.color.rgb = rgb("C00000")
                box.text_frame.paragraphs[0].font.size = Pt(18)
                item = f"Slide {n}: graph '{question.strip()}' missing (expected {png.name})"
                missing.append(item)
                all_open.append(item)

        notes = [f"Sources: {s.get('Sources', 'not given')}"]
        affecting = s.get("Open questions", "none")
        if affecting.lower() != "none":
            notes.append(f"Open questions: {affecting}")
            new = strip_known(affecting, outline_open)
            if new:
                all_open.append(f"Slide {n}: {new.strip(' ;')}")
        slide.notes_slide.notes_text_frame.text = "\n".join(notes)

    # Paginate open items by estimated text height so no page overflows the body section.
    item_size, budget = 14, body_h - Inches(0.4)
    pages, page, used = [], [], 0
    for item in all_open:
        h = text_height(item, text_w, item_size) + int(Pt(10))
        if page and (used + h > budget or len(page) >= OPEN_ITEMS_PER_SLIDE):
            pages.append(page)
            page, used = [], 0
        page.append(item)
        used += h
    if page:
        pages.append(page)
    for i, page in enumerate(pages, 1):
        title = "Open items" + (f" ({i}/{len(pages)})" if len(pages) > 1 else "")
        slide = base_slide(prs, style, title, subheader)
        add_text(slide, text_left, body_top, text_w, body_h, page, item_size, style["body"],
                 NEAR_BLACK, anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER, space_after=10)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    prs.save(OUT)
    print(f"wrote {OUT.relative_to(ROOT)} with {len(slides)} slide(s)"
          f" + {len(pages)} open items slide(s) ({len(all_open)} item(s))")
    for item in missing:
        print(f"WARNING {item}")
    return 0


if __name__ == "__main__":
    sys.exit(build())
