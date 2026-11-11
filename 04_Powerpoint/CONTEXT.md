# Powerpoint

Assembles the finished presentation. Takes the outline, the sourced information, the brand rules and any graphs, and produces one PowerPoint file. This stage adds no new facts. Where something the outline needs is missing, it shows the gap on the slide and lists it under open questions. It does not fill the gap.

Paths below are relative to the workspace root.

## Reads

- **Slide plan (working):** `02_Processing/output/outline.md`, in the fixed `## Slide N` format. Slide order, titles, messages, sources, the `Graph` line and open questions of each slide.
- **Facts (working):** `01_Intake/output/information.md`. Every number and quote on a slide must appear here.
- **Graphs (working, optional):** `03_graphs/output/graphs/<name>.png`, where `<name>` is the data file named in the slide's `Graph` line. If a PNG is missing, the slide shows it as missing.
- **Reference (every run):** `constraints/brand.md` (colors, fonts, layout style, logo). `TODO` fields are not guessed. They are shown as open items.
- **Tools (every run):** `_tools/CONTEXT.md`, the catalog of shared scripts.

## Process

1. Read the outline, the information file, the brand rules, and the graph manifest, in that order.
2. Use the build script `04_Powerpoint/_tools/build_deck.py`, using python-pptx. It creates one slide per `## Slide N` entry, in outline order, with the brand fonts and colors. If the script is missing, write it to this exact behaviour first.
3. For each slide the script:
   - Puts the title and message on the slide.
   - Puts the graph on the slide if the `Graph` line names one.
   - Shows a visible `GRAPH MISSING: <question>` box if the graph is named but its PNG is missing, and reports it.
   - Puts the sources and the slide's open questions in the speaker notes.
4. Run the script from the workspace root: `python3 04_Powerpoint/_tools/build_deck.py`. Do not edit the deck by hand. To change it, change the outline or the script and run again.
5. Adds a final "Open items" slide, listing the outline's open questions and every open question from the slides, if there are any.

## Writes

- `04_Powerpoint/_tools/build_deck.py` (the build script, kept so the deck can be rebuilt)
- `04_Powerpoint/output/presentation.pptx` (the deck)

## Check

person: the slide count and order match the outline; every title and message matches the outline; every number and quote on a slide appears in `information.md`; every graph sits on the slide its `Graph` line names, and each missing graph is listed under open questions; colors and fonts match `constraints/brand.md`; no `TODO` text and no `GRAPH MISSING` box remains unless its item is listed under open questions; the speaker notes list the open questions that affect each slide.

Optional machine check later: a `check.md` whose first line is `pass` or `fail: <why>`.