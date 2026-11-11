# Intake

Take the information the person provides in a Markdown file and save it as clean, sourced notes. Later stages decide the structure and turn the information into slides, so this stage writes no outline, storyline or slide content, and does no research of its own.

## Reads

- **This run's input (working):** every file the person places in `input/` inside this stage folder, whatever its type (see the table under Process).
- **Reference (every run):** none yet. `TODO: add reference files here once they exist`

## Process

1. List every file in `input/`. For each file, record its name, type, and size in `output/input_profile.md`, and mark what kind of content it holds: text, facts, quotes, data, or images. Then read each file according to its type:

| Type | How to read it | What to record |
|---|---|---|
| `.md`, `.txt` | Read completely | Facts, figures, quotes |
| `.csv` | Read the header and every row | Column names, units from headers, row count. Mark as data for the graphs stage. |
| `.xlsx`, `.numbers` | Do not convert. Mark as not read | "Export this sheet as CSV into input/" |
| `.pdf`, `.docx` | Extract the text if a tool for it is available. Otherwise mark as not read | Facts found, or "not read: ask the person for Markdown" |
| Images | Describe only what is clearly visible | Description, or "not read" if unclear |
| Anything else | Do not guess | "Not read: unsupported type" |

Ask nothing: mark a file as not read and carry on.
2. Record each fact, figure, quote or claim as its own entry: the statement in your own words, and its source (the file name and the section or line where it appears).
3. Keep statements exactly as they relate to the input. Do not add anything the input does not say.
4. Flag anything that is unclear, contradictory or incomplete under "Open questions". Do not guess to fill gaps.
5. Do not write slide titles, slide order, a storyline or any slide text.

## Writes

`output/input_profile.md`: one line per input file (name, type, what it holds, read or not read).

`output/information.md`, with these sections in this order:

- **Topic and purpose** (as stated in the input)
- **Information** (grouped by topic; each entry with its source)
- **Open questions**

## Check

person: every file in `input/` appears in `input_profile.md` with its type and read status; every statement in the input appears under "Information", every entry names its source, there are no slide titles or storyline, and every gap appears under "Open questions". The reviewer compares `output/information.md` with the file in `input/`.

Optional machine check later: a `check.md` whose first line is `pass` or `fail: <why>`.