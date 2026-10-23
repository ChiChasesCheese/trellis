# Diagram task — make every diagram readable on a phone

Repo `/Users/chiserver/sessions/trellis`, branch `main` (never switch branches, never commit, never spawn agents).

Chi reads these pages in Obsidian on an iPhone. A code block wraps at about 40 monospace columns, and CJK glyphs are not
exactly two cells wide, so wide ASCII diagrams and box diagrams with Chinese labels fall apart.

Read `proposals/WRITING_RULES.md` rules 9 and 12. Check your files with:

    python3 scripts/phone_diagrams.py <files…>     # must print ok
    python3 scripts/plain_style.py <files…>        # must still print ok

For every flagged diagram, redraw it in the first form that fits:
1. **Table** — when the diagram is really rows × columns (layouts, timelines with values, comparisons, memory hierarchies).
2. **Numbered / nested list** — when it is a sequence of steps or a hierarchy.
3. **Mermaid** within rule 9 (`flowchart TB`, ≤ 12 nodes, ≤ 4 side by side, labels ≤ 16 chars; `sequenceDiagram` with the
   init line, `autonumber`, ≤ 5 participants, messages ≤ 24 display units, numbered steps explained in a list below).
   Chinese labels are fine inside mermaid nodes.
4. **Narrow ASCII** (≤ 40 columns, ASCII only on drawing lines) with a legend list or table underneath for the Chinese
   labels — for bit layouts, ring buffers, arrays with indices, pointer pictures.

Keep the information identical (every value, label and arrow meaning). Do not touch code blocks in a programming
language, program-output blocks without drawing characters, or any file on disk other than the `.md` pages you own.

Final reply ≤ 6 lines: files fixed, diagrams redrawn by kind (table / list / mermaid / ascii), anything left.
