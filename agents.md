---
icm: true
---
# Präsentationen

This workspace turns sourced information into a finished, on-brand PowerPoint presentation. It holds routing and rules only. The content lives in the stage folders and the reference folders.

## Where am I

Numbered folders are stages, run in order. Each stage folder holds `CONTEXT.md` (its contract), `input/` (the material for this run), `output/` (what the stage produced), and optionally `check.md` (a verdict).

## Where do I go

| Task | Go to |
|---|---|
| Set or change brand name, colors, fonts, layout | `constraints/CONTEXT.md`, then `constraints/brand.md` |
| Provide information for a new presentation | `01_Intake/CONTEXT.md`; put material in `01_Intake/input/` |
| Turn information into a slide outline | `02_Processing/CONTEXT.md` |
| Make graphs from data (optional) | `03_graphs/CONTEXT.md`; data goes in `03_graphs/input/` |
| Build the PowerPoint | `04_Powerpoint/CONTEXT.md` |
| Shared scripts and how to run them | `_tools/CONTEXT.md` |

## Order

Run `01_Intake`, then `02_Processing`, then `03_graphs` (optional), then `04_Powerpoint`. Each stage reads the output of the one before it.

## Rules

- Stages add no facts beyond their inputs. Each stage's `## Check` section says how its output is verified.
- `constraints/` and `_tools/` are reference material shared by every run. Per-run material goes into a stage's `input/`.
- Do not hand-edit generated outputs. Change the input or the script and run the stage again.
- Status lives on disk: the TUI reads each stage's `output/` and `check.md`.