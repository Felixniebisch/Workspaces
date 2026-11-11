# Tools

Catalog of the shared scripts in this workspace. Each entry says what the script does, how to run it, and what it needs installed. Scripts that belong to one stage live in that stage's own `_tools/` folder and are listed in that stage's `CONTEXT.md`, not here.

Paths below are relative to the workspace root.

## Reads

- None. This file lists tools. It processes no data.

## Process

1. Find the tool you need in the table below.
2. Check that its dependencies are installed.
3. Run its command from the workspace root.
4. Do not edit a tool during a stage run. Change it in a separate step and note the change.

## Writes

- None.

## Tools

| Script | What it does | Command | Dependencies | Status |
|---|---|---|---|---|
| `_tools/links.py` | Walk test: checks that links and input paths resolve | `python3 -I _tools/links.py` | Python 3 standard library | TODO: not copied into this workspace yet |
| `_tools/index.py` | Rebuilds `_index.md` from the notes | `python3 -I _tools/index.py` | Python 3 standard library | TODO: planned for phase 3 |

## Check

person: every script in the table exists in `_tools/` with the stated command; every dependency is installed; no script writes outside the folder it reports.
