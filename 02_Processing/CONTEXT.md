# Processing

Turn the sourced information from the intake stage into a slide outline: one entry per slide, with its message and the information it uses. The next stage builds the PowerPoint from this outline. This stage adds no facts and writes no slide design.

Paths below are relative to the workspace root.

## Reads

- **This run's input (working):** `01_Intake/output/information.md` and `01_Intake/output/input_profile.md`. The profile says what kind of material the run has, and whether any data exists for graphs.
- **Reference (every run):** `constraints/brand.md` (brand name, colors, fonts, layout style). Use these values for every slide entry's design notes. If a field there is still `TODO`, record it under "Open questions" and do not guess.
- **Tools (every run):** `_tools/CONTEXT.md`, the catalog of shared scripts. This stage normally runs no script; use one only if the outline needs it.

## Process

1. Read `01_Intake/output/information.md` completely.
2. Read the "Topic and purpose" section first. It sets the goal and the audience for the whole outline.
3. Choose the storyline: a short sequence of messages that together support the goal. Write each message as one full sentence.
4. For each message, write one slide entry in the exact format below. Use one line per field. Write a graph only where the profile lists a data file for it. Without any data file in the profile, every Graph line is `none`.
5. Use only entries that exist under "Information". Do not add facts, figures or quotes.
6. Carry every item from "Open questions" into the outline's own "Open questions", so no gap is lost before slides are built.
7. Propose a slide count from the audience, the length in the input, and the amount of information: a thin input gets fewer slides. If the input gives no length, write "not specified" and do not guess.
8. If the profile lists files marked as not read, carry that into "Open questions" so the person can supply them.

## Slide format

Each slide is a level-2 heading `## Slide N` (N counts from 1), followed by these fields, one line each:

```
## Slide 1
- Title: <short slide title>
- Message: <one full sentence>
- Sources: <information entries used, by their statement's short label>
- Graph: none | <question the graph answers> | data: <file name>.csv
- Open questions: none | <question>
```

The `Graph` value is `none`, or the question, a vertical bar, then `data:` and the CSV file name the person provides in `03_graphs/input/`. Do not write more than one graph per slide.

## Writes

`02_Processing/output/outline.md`, with these sections in this order:

- **Goal and audience** (copied from the intake's "Topic and purpose")
- **Storyline** (the messages in order, one sentence each)
- **Slides** (one `## Slide N` entry per slide, in the format above)
- **Open questions** (all gaps carried over from intake, plus any found while outlining)

## Check

person: every slide uses only entries from `01_Intake/output/information.md`; every entry in "Information" that matters to the goal appears on at least one slide; every open question is carried into "Open questions"; every slide whose Graph line is not `none` names a question and a data file; no slide contains a fact without a source entry; the outline has a slide count or says "not specified".

Optional machine check later: a `check.md` whose first line is `pass` or `fail: <why>`.