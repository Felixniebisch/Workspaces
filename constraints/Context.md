# Constraints

Holds the brand rules every presentation in this workspace must follow: the brand name, colors, fonts, and layout style. These files are reference material. They are set up once and read by later stages on every run. They are not regenerated per presentation.

## Reads

- **Setup answers (working, only during setup):** the answers the person gives to the questions in this file.
- **Current rules (reference):** `constraints/brand.md`, if it already exists.

## Process

This setup asks questions, so run it interactively in Claude Code. The TUI runs stages headless, where questions cannot be answered.

Setup run (when `constraints/brand.md` is missing or the person asks to change it):

1. Ask the person, one group at a time, for: brand name; primary, secondary and accent colors as hex codes; font for headings and for body text; layout style (for example minimal, corporate, or editorial), with a one-line description; whether a logo is used, and where it sits.
2. Do not invent values. If an answer is missing, leave the field as `TODO` and say so.
3. Write `constraints/brand.md` in the structure below.
4. Show the person the finished file and ask for approval before the setup is considered done.

Update run (when the file exists and the person asks for a change):

1. Change only the fields the person names.
2. Keep the rest of the file as it was.

## Writes

`constraints/brand.md`, with these sections in this order:

- **Brand name**
- **Colors** (name, hex code, and where to use it)
- **Fonts** (headings, body)
- **Layout style** (name and a one-line description)
- **Logo** (used or not, placement)
- **Open items** (every field still set to `TODO`)

## Check

person: every field has a value or is listed under "Open items"; every color is a valid hex code; the file has no values the person didn't give; the person approved the file.