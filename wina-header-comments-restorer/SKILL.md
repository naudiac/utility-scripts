---
name: wina-header-comments-restorer
description: Restores stripped threaded comments from the GWS report headers by injecting them as standard legacy notes. Reads from a customizable JSON config.
---

# wina-header-comments-restorer

This skill restores the header comments (BS1 and EN1) in the WINA GWS report that are routinely stripped out by openpyxl due to its lack of support for modern threaded comments. It injects them as standard legacy notes, which prevents future scripts from stripping them out again.

## Usage
Trigger this when the user asks to "restore the header comments in the GWS report" or similar.

Run the script like this:
`ash
python scripts/restore_comments.py "path_to_excel_file.xlsx"
`

## Altering the Notes
If the user wants to alter the text of the notes, direct them to edit the file at esources/comments_config.json. They do not need to modify the Python code.
