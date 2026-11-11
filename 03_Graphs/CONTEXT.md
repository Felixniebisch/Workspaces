# Graphs

Optional stage. Turns the data in this stage's `input/` into graphs for the slides that need them, using the brand colors. If no data file is provided, the stage records that it was skipped, and the later stages carry on without graphs.

Paths below are relative to the workspace root.

## Reads

- **This run's data (working):** data files in `03_graphs/input/` (CSV). `01_Intake/output/input_profile.md` lists which data files the intake saw, so the two can be compared.
- **Slides that need graphs (working):** `02_Processing/output/outline.md`, the slide entries whose `Graph` line is not `none`. Those lines name the question each graph answers and the data file to use.
- **Reference (every run):** `constraints/brand.md` (colors, fonts). If the file's colors are still `TODO`, use neutral grays and record this under "Open questions".

## Process

1. Check `03_graphs/input/`. If it contains no data file, write `03_graphs/output/graphs.md` with one line, `Skipped: no data files in input/`, and stop.
2. Read each data file completely. Check the columns, units, and any missing values. Record each problem under "Open questions" and do not fix data silently.
3. From the outline, list each slide whose `Graph` line is not `none`, with the question the graph has to answer. Do not add graphs the outline does not ask for. If a named data file is missing from `input/`, record it under "Open questions" and skip that graph.
4. Write one plotting script, `03_graphs/_tools/make_graphs.py`. It reads the data files and the colors from `constraints/brand.md`, and writes one PNG per graph to `03_graphs/output/graphs/`. Every chart has a title, labelled axes with units, and a source line.
5. Run the script from the workspace root: `python3 03_graphs/_tools/make_graphs.py`. Do not hand-edit the PNGs. To change a graph, change the script and run it again.
6. Write `03_graphs/output/graphs.md`: one entry per graph with the slide it belongs to, the PNG file name, the data file and the columns it used, and any open questions about it.

## Writes

- `03_graphs/_tools/make_graphs.py` (the script, kept so the graphs can be rebuilt)
- `03_graphs/output/graphs/*.png` (one file per graph)
- `03_graphs/output/graphs.md` (manifest: slide, file, data source, open questions)

## Check

person: every graph in `graphs.md` matches a slide in the outline; each graph's numbers can be traced to the columns named in its entry; no value was typed by hand into a PNG; axes are labelled with units; colors come from `constraints/brand.md`; the stage's skip note is present if no data was provided.

Optional machine check later: a `check.md` whose first line is `pass` or `fail: <why>`.