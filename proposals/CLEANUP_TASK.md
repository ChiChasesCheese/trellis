# Cleanup pass — learning pages carry only what to study (Chi, 2026-10-17)

Read `proposals/WRITING_RULES.md` first; it wins. Chi's words: 「完全不要提到来源；所有文章都变成能用来背/学习的
action item；只看关键信息，不展示任何 discovery / preparation 过程。」 The earlier pass moved provenance to a last
「来源」 section — that is now wrong too: **delete every 来源 / 来源与延伸 / 来源与延伸阅读 / 证据 / 依据 section and every
`> 来源` line**. Their content is already saved in `research/companies/amazon/PROVENANCE.md` — you do not need to keep it.

## What a clean page looks like

- First lines: `# <title>` (append `（low priority）` if your task says so), then 3–5 plain sentences on what the topic is
  and why it matters for the interview, then the content.
- Body: facts, decisions with their reasons, steps, code, questions to practise and the answers to rehearse. Delete
  anything about how the page was made, what sources say, which parts were reconstructed, confidence, coverage, counts of
  reports, "kit", "this file", "Chi 的…"(write 「你」 instead), process checklists for maintainers, run commands for gates.
- Where a page explained *why a question is likely* using report counts, replace it with nothing — or, if the priority
  matters, with the `（low priority）` title label.
- Optional last section `## 延伸阅读`: study links only (related notes as wikilinks, docs, tutorial pages), no commentary
  about sources.
- Diagrams per WRITING_RULES §9. Keep all code, numbers that are part of the content (capacity estimates, complexities,
  examples), and answers. Do not shorten content to make it "cleaner" — only remove process and provenance, and fix voice.
- Fix every relative link that points into `../catalog/`, `../tools/`, `CHECKPOINT`, `AGENT_RULES`, `SD_TASK` — those moved
  out of the vault; delete the reference. Kit paths changed on 2026-10-17: system design is now
  `vault/interviews/core/system-design/amazon/`, coding is `vault/interviews/core/coding/amazon/`, LLD is the
  low-level-design domain's `amazon` branch (notes `solution-amz-*`). Prefer wikilinks by note name — they survive moves.

## Checks before you report

- `python3 scripts/plain_style.py <your files>` → `ok` (LP pages: add `--outline`).
- `python3 scripts/check_wikilinks.py <your folder relative to vault/>` → no dead link in your files.
- Any gate your task names. Every `.py` you touched still runs.

Touch only the files your task names. Do not run git. Do not start agents. Report ≤ 8 lines: checks run and anything you
could not fix.
