# Rewrite pass — make existing pages follow proposals/WRITING_RULES.md (Chi, 2026-10-16)

Chi read the first pages and asked: provenance (帖子编号、日期、置信度、（重建）、平台名) only at the end of a page if
at all; every page in plain words, textbook level, cause and effect, self-contained, no third-person narration; and
diagrams that fit Obsidian's column (a wide `flowchart LR` got cut off). Read `proposals/WRITING_RULES.md` first.

This is a **rewrite, not a new write-up**. Keep every fact, number, code block, test, card id, card `step`, file name and
wikilink target. Do not shorten content to pass a length check; the gates' minimums still apply.

## What to change, per artifact

- **Article / write-up / study note.**
  1. Open with the system in plain words (3–5 sentences: what it is, who uses it, what is hard), then the problem as an
     interviewer would pose it to you. No quotes from posts, no dates, no platform names, no 「（重建）」「推断」 labels.
  2. Move every piece of provenance into the final section (`## 来源与延伸` in LLD articles, `## 来源与延伸阅读` in SD
     write-ups, `## 来源` in study notes): which platform/thread/report, date, level, confidence, which stages or
     requirements were reported and which were added, and the further-reading links (Hello Interview: what it does, where
     this page differs). Write that section as a short list, plain.
  3. Re-read every paragraph and fix the voice: no 本篇/本文/本题/本题解/这道题/作者/我们/候选人/楼主/报告. Talk to the
     reader or explain plainly.
  4. Add the missing *why*: every 「用 X」 gets what forces it and what it costs. Every term of art gets a one-line plain
     definition the first time.
  5. Self-contained: replace 「见 XX」 for a fact the argument needs with the fact itself (keep the link as further reading).
  6. Diagrams: `flowchart TB` only, ≤ 12 nodes, labels ≤ 16 chars, ≤ 4 nodes per row; split an architecture into a
     write-path and a read-path diagram; classDiagram ≤ 8 classes (drop helper/exception classes, list them in prose);
     sequenceDiagram ≤ 5 participants.
  7. LLD articles: the code block between `%% code:begin %%` markers is generated — never edit it by hand; if you
     change a docstring in `solution.py`, re-run `uv run python scripts/lld_embed_code.py <slug>` and the tests.
- **Drill.** Plain problem statement and stages; no provenance words at all (the article's last section has them).
- **Card** (`vault/domains/low-level-design/cards/amazon/<id>.md`, or an entry of a cards JSON). Edit the file in place
  — do not re-import, do not change `id`, `node`, `step`, `type`. No provenance words on the card. The step-1 card's
  front becomes 「<题名>要你设计什么？开场先问哪三个澄清问题？」 (LLD) or a plain problem question (coding). A coding card's
  `meta` is at most difficulty + 「Amazon 2026-10」; its `sources` list (footer links) keeps the provenance.

## Gates (must pass before you report)

- LLD leaf: `uv run python scripts/check_lld_problems.py --branch amazon <leaf id>` → `ok` (includes the style check),
  and `uv run trellis --domain low-level-design validate` shows no error naming your files.
- SD write-up: `python3 scripts/check_sd.py <sdNN>` → `ok`.
- Coding notes / cards: `python3 scripts/plain_style.py <notes...> <cards.json>` → `ok`; every `.py` still runs.

Touch only the files your task names. Do not run git; do not start agents. Report ≤ 8 lines: gate lines, and anything you
could not move or fix.
