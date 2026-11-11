# Graphs

Built by `03_graphs/_tools/make_graphs.py` (run: `python3 03_graphs/_tools/make_graphs.py` from the workspace root).

No graphs this run: every slide in `02_Processing/output/outline.md` has `Graph: none`, so the script made no PNGs. The stage does not add graphs the outline does not ask for.

## Data files checked

| File | Columns | Rows | Problems |
|---|---|---|---|
| `03_graphs/input/resolved_by_support_chat.csv` | `Group`, `Issue resolved (%)` | 2 (Used support chat 81; Did not use support chat 64) | No missing values. No group sizes. |
| `03_graphs/input/unclear_by_area.csv` | `Area`, `Unclear answers (%)` | 4 (Invoicing 27; Delivery 9; Support 6; Contract changes 4) | No missing values. |

## Open questions

1. **Outline and data disagree.** `03_graphs/input/` has two CSV files, but the outline asks for no graphs. Its open question 10 says the intake listed no data file. `01_Intake/output/input_profile.md` lists only `example.md` too, so the intake never saw these CSVs. If the charts are wanted, re-run 01_Intake and 02_Processing so the slides get Graph lines in the form `- Graph: <question> | data: <file.csv>`. These would fit slide 4 (`unclear_by_area.csv`) and slide 5 (`resolved_by_support_chat.csv`). Then run this stage again.
2. **Stale PNGs.** `03_graphs/output/graphs/` still has `resolved_by_support_chat.png` and `unclear_by_area.png` from an earlier run, when the outline asked for graphs. This run did not make them and they are not part of it. They were not deleted. 04_Powerpoint should go by this manifest and not use them. Delete them by hand if they are not wanted.
3. **Unsourced values.** `unclear_by_area.csv`: the 27 % for Invoicing matches the intake. Delivery 9 %, Support 6 % and Contract changes 4 % do not appear in the intake material, so their source needs to be confirmed. They also look like a partial answer to outline open question 5 (scores of other areas). The figures measure the share of unclear answers, not a rating.
4. **Chat comparison.** `resolved_by_support_chat.csv` has no group sizes. Possible duplicate tickets were not checked. The period mismatch between the support log and the survey (outline open questions 1, 3 and 4) is still open.
5. **Fonts.** If graphs are made later, the brand colors come from `constraints/brand.md` (primary #2E6061). Abril Fatface and Lato may not be installed, in which case matplotlib uses its default font.
6. **Path casing.** The contract writes `03_graphs/` and `constraints/`, but the folders on disk are `03_Graphs/` and `Constraints/`. The script finds its paths from its own location and matches the folder names regardless of case.
