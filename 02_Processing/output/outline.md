# Outline: Customer Survey Results, Q3

## Goal and audience

- **Topic:** Customer survey results, Q3.
- **Purpose:** Inform the leadership team about the Q3 customer survey and propose two actions for Q4.
- **Audience:** Leadership team of Fiktive GmbH: five people with a technical background who are short on time.
- **Length:** About 10 minutes. No slide count is given.
- **Proposed slide count:** 6 slides (about 1.5 minutes each). The input is short and the audience is short on time, so the deck stays small.

## Storyline

1. Customer satisfaction is up in Q3, but invoicing is the weak spot.
2. The survey ran from 1 to 20 September, reached 1,240 customers, and 412 of them answered.
3. Overall satisfaction rose from 3.8 in Q2 to 4.1 in Q3 on a 5-point scale.
4. Invoicing is the lowest-rated area: 27 % of respondents said their invoices were unclear.
5. Customers who used the new support chat rated their issue as resolved more often, 81 % vs. 64 %.
6. For Q4 we propose a simpler invoice layout and keeping the support chat while extending it to invoicing questions.

## Slides

## Slide 1
- Title: Q3 customer survey: satisfaction up, invoicing the weak spot
- Message: Customer satisfaction is up in Q3, but invoicing is the weak spot.
- Sources: Key message wish; Satisfaction trend; Weakest area
- Graph: none
- Open questions: The input is marked "EXAMPLE, fictional data"; confirm whether this is a test run or whether real data will replace it.

## Slide 2
- Title: Who we asked
- Message: The survey ran from 1 to 20 September, reached 1,240 customers, and 412 answered, a response rate of about 33 %.
- Sources: Survey period; Reach; Responses
- Graph: none
- Open questions: The response rate for enterprise customers is missing from the survey sheet.

## Slide 3
- Title: Satisfaction is up
- Message: Overall satisfaction rose from 3.8 in Q2 to 4.1 in Q3 on a 5-point scale.
- Sources: Satisfaction trend
- Graph: none
- Open questions: Q2 sample size and response rate are not given, so the comparability of Q2 and Q3 is unclear.

## Slide 4
- Title: Invoicing is the weak spot
- Message: Invoicing is the lowest-rated area: 27 % of respondents said invoices were unclear, and one customer wrote "The invoice has three numbers and I still don't know which one I pay."
- Sources: Weakest area; Unclear invoices; Customer quote on invoices
- Graph: none
- Open questions: The score for invoicing and the scores of the other areas are not given.

## Slide 5
- Title: The support chat helps
- Message: Customers who used the new support chat rated their issue as resolved more often: 81 % vs. 64 %.
- Sources: Chat resolution rate
- Graph: none
- Open questions: Possible duplicate tickets in the chat numbers (not checked); the 64 % comparison group and the group sizes are not stated; the support log (3 to 18 September) and the survey (1 to 20 September) cover different periods and it is not stated how they were matched.

## Slide 6
- Title: Two actions for Q4
- Message: For Q4 we propose a simpler invoice layout, and keeping the support chat while extending it to invoicing questions.
- Sources: Proposal 1; Proposal 2; Unclear invoices; Chat resolution rate
- Graph: none
- Open questions: none

## Open questions

Carried over from intake:

1. **Possible duplicate tickets:** The author thinks the support chat numbers include some duplicate tickets but has not checked this. The 81 % vs. 64 % comparison may be affected.
2. **Enterprise response rate missing:** The response rate for enterprise customers is missing from the survey sheet.
3. **Comparison group for the chat figure:** The input does not say explicitly who the 64 % refers to (presumably customers who did not use the chat), nor how many customers are in each group.
4. **Chat period vs. survey period:** The support log export covers 3 to 18 September; the survey ran 1 to 20 September. It is not stated whether the two data sets cover the same customers or how they were matched.
5. **Ratings of other areas:** Invoicing is called the lowest-rated area, but its score and the scores of the other areas are not given.
6. **Q2 baseline:** The Q2 satisfaction score is given, but not Q2's sample size or response rate, so comparability of the two quarters is unclear.
7. **Underlying sources not provided:** The survey sheet and the support log export are cited but not in `input/`. If charts are wanted, they would need to be exported as CSV into the input of the graphs stage.
8. **Fictional data:** The input is marked "EXAMPLE, fictional data". Confirm whether this is a test run or whether real data will replace it.
9. **Stray character:** Line 26 ends in "questions.y". This looks like a typo and is read as "questions".

Found while outlining:

10. **No graphs:** The input profile lists no data file, so every Graph line is `none`. The figures on slides 3 to 5 (satisfaction trend, unclear invoices, chat resolution) would suit charts if CSV data is supplied in `03_Graphs/input/`.
11. **Design notes field:** The contract says to use the brand values from `constraints/brand.md` for each slide entry's design notes, but the slide format has no design-notes field. No such field was added. The brand values apply to every slide: brand name GEM-example; colors Primary #2E6061, Secondary #50453E, Accent #837651; fonts Abril Fatface (headings) and Lato (body); professional layout with square corners, high-contrast copy, a subheader under every heading, centered body content; "GEM-example" logo text in 6 pt in the accent color in the corner. Please confirm whether a design-notes field should be added to the format.
12. **Path casing:** The contract refers to `constraints/brand.md`; on disk the folder is `Constraints/`. The file was read from there.
