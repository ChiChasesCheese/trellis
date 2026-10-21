# Style task — make Headlands learning pages pass WRITING_RULES

Repo `/Users/chiserver/sessions/trellis`, branch `main` (never switch branches, never commit, never spawn agents).

Read first: `proposals/WRITING_RULES.md` (the rules) and `scripts/plain_style.py` (the machine check).

Run the check on your files: `python3 scripts/plain_style.py <files…>` (behavioral / LP-style pages: add `--outline`).
Goal: **every file you own passes**, and the rules the script cannot check are also met:

- Rule 1: no provenance or process anywhere. Study links only in a final `## 延伸阅读` section (replace any 「延伸」 line
  with that heading if it holds a link; a pure "next lesson" pointer line may stay as plain text).
- Rule 3: no 本篇 / 本文 / 本题 / 这道题 / 我们认为 — talk to the reader («你») or plainly state the fact.
- Rule 5: a term is defined in one plain line on first use, English name in full-width parentheses.
- Rule 6: self-contained.
- Rule 7: open with the topic in plain words (3–5 sentences) before any list or table.
- Rule 9: mermaid diagrams within the limits (the script reports violations).
- Rule 10 (behavioral pages only): outlines only — bullets, no paragraphs; stories as headline + S/T/A/R/L bullets with
  bold keywords; questions as framework + beats + 2–4 follow-ups with one-line cues; placeholders as 【待补：…】.
- Do **not** add `（low priority）` labels (Chi has not approved them for this kit).
- Hex strings the script flags inside **program output** (addresses, hashes printed by a demo) are not provenance, but the
  script still fails on them: shorten or redact them in the prose copy (e.g. `0x16f…a8`) — never edit code files.
- Code blocks that mirror files on disk (`reference/`, `cpp/`, `examples/`, `demos/`, `solutions/`) stay byte-identical,
  except you may redact a flagged hex value inside a quoted *output* block.
- Keep every teaching point, code block, follow-up and self-check; this is a style pass, not a content cut.

Final reply ≤ 8 lines: files passing before/after (from the script), anything you could not fix and why.
