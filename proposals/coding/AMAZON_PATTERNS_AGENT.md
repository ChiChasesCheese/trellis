# Amazon coding patterns — clean the lectures, then cards for deck `LeetCode Tops::23 Amazon 模式强化（patterns）`

Chi studies the Amazon A-tier deck (`LeetCode Tops::20`, whole-problem cards for 239 problems) first; deck 23 is the
reinforcement after it: the 16 patterns as concepts, plus whole-problem cards for the kit problems the A tier lacks.
Read `proposals/WRITING_RULES.md` and `proposals/CLEANUP_TASK.md` first. Repository root `/Users/chizhang/Code/trellis`.

Folder: `vault/interviews/core/coding/amazon/` — `patterns/01…16_*.md` (lectures), `solutions/*.py` (tested solutions),
`run_all.py` (runs every solution and checks that a lecture block whose first line is `# solutions/<file>.py` appears
verbatim inside that file's `# --- solution ---` … `# --- end ---` region), `plan.md`, `amazon_bar.md`, `top_list.md`,
`recent/amz_*.md` (+ `recent/code/*.py`).

## 1. Clean your lectures (WRITING_RULES + CLEANUP_TASK)

Delete provenance and process (report ids like LC8293563 / RD… / JC…, counts of reports, "#refs", URLs of posts, 来源
sections, maintainer notes, run commands for checks). Keep the teaching: recognition signals, templates, traces, pitfalls,
complexity, the problems with their solutions. Start each lecture with 3–5 plain sentences on the pattern. Keep every
code block byte-identical (run_all checks them).

## 2. Cards — one JSON file you own, list order = study order

Schema per card: `{"id", "slug", "title", "meta", "question_md", "answer_md", "note"}`.
- `id`: `amp-<two-digit pattern>-<short-slug>`; `slug`: same without the prefix; `note`: vault-relative path of the
  lecture (e.g. `interviews/core/coding/amazon/patterns/05_heap_top_k.md`).
- `meta`: difficulty or `模式` · nothing else (no provenance, no "Amazon 报告").
- `answer_md`: paragraphs starting `思路｜`, `模板｜`, `复杂度｜`, `易错｜`, `追问｜` become chips; ```python blocks
  ≤ 25 lines that appear verbatim in `solutions/*.py` or in a lecture code block.

Per pattern, in this order:
1. **识别信号** — 「什么样的题该想到 <pattern>？」: 3–4 concrete signals, each with a one-line example problem.
2. **模板** — the reusable code skeleton (from the lecture), with what each variable means.
3. **易错点** — the mistake that costs the round, with a concrete input and the wrong vs right output (run it).
4. **常见追问** — 2–3 follow-ups interviewers add on this pattern and the one-line answer each.
5. Whole-problem cards (front: statement + constraints; back: 思路 / code / 复杂度 / 追问) for every problem of this
   pattern in this list — the kit problems the A-tier deck does not have: LC 10, 1235, 134, 211, 297, 312, 341, 348, 435,
   588, 68, 721, 73, 871. Put each under the pattern its lecture teaches it in.

Constraints on cards come from the problem statement (WebFetch leetcode.com/problems/<slug>/ or leetcode.cn), never from
memory. No 本题/这道题 — name the problem.

## Checks

- `python3 -I vault/interviews/core/coding/amazon/run_all.py` → ALL PASS.
- `python3 scripts/plain_style.py <your lectures> <your cards json>` → ok.
- Every card code block appears verbatim in a solution or lecture (`python3 -c` it).
- `uv run --with markdown --with pygments python scripts/amazon_push_cards.py --set patterns --dry-run` lists your cards.

Do not push to Anki, do not run git, do not start agents. Touch only your files. Report ≤ 8 lines.
