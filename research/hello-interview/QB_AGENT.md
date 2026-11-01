# Card agent — Hello Interview 高频真题 (question bank), one complete answer per question

Repo `/Users/chiserver/sessions/trellis`, branch `main`. Never commit, never spawn agents, write only your files.
Scratch in `/tmp/qb_<group>/`. `git checkout uv.lock` whenever uv touches it. **Resume rule:** skip a question whose
body already exists.

Chi (2026-11-01): the high-frequency design questions matter most. Treat each like a LeetCode whole-answer card: the
complete answer, the intuition behind every decision, the techniques it uses, and links to the concepts it rests on
(the course part of the deck is its prerequisite deck).

## Input

Your questions are slugs in your group file. Source: `sources/local/hello-interview/qb/<slug>.md` — the question, every
candidate report (company, level, month, often the interviewer's twist or scale numbers), and for some questions the
free problem-breakdown page. Where there is no breakdown, design the answer yourself to the senior bar, using the
reports' constraints. Concepts you can link: `research/hello-interview/concept_index.md`. Chi's other design material
(link when it covers the same system): `vault/domains/system-design/problems/` and `vault/domains/low-level-design/problems/`.

## Output 1 — the shared body (one file per question, the single source of truth)

`vault/interviews/core/design-questions/<slug>.md`, frontmatter only `slug: <slug>` and `kind: <system-design|low-level-design>`:

```
## Q
**<中文题名>**｜<系统设计|低层设计>

<the question restated in Chinese, with the scale numbers and twists the reports mention>

给出完整解答：需求、核心实体与接口、整体设计、深入问题、取舍、不同级别的期望。

## A
**一句话。** the crux of this question in one sentence (what makes it hard)
**需求。** functional (3–5) and non-functional with numbers (QPS, storage, latency, consistency)
**核心实体与接口。** entities; the key API calls (system design) or classes and responsibilities (low-level design)
**整体设计。** the main flow end to end, component by component; a small ```svg diagram if it reads faster (phone width)
**深入。** 2–4 deep dives; each: the problem → the options with their cost → the choice and why
**取舍与追问。** the follow-ups interviewers push (from the reports when present) and how the design changes
**级别期望。** what mid / senior / staff should cover, one line each
**先修概念。** wikilinks from concept_index.md (`[[hi-...|名字]]`), 3–6
**同类题。** 2–4 related questions or breakdowns, wikilinks where a note exists
```

Low-level design: in **核心实体与接口**, the classes; add a ```python block with the core class skeleton and the one or
two key methods implemented (type hints; Chinese comments carry the reasoning), plus the pattern used and why.

Chinese throughout, English terms in parentheses on first use. Own words only — never copy sentences from the source
(commercial site, public repo); facts and numbers are fine. Long is fine; every sentence must carry a fact or a reason.
No URLs, no "Hello Interview 认为", no process talk.

## Output 2 — metadata for the deck

`research/hello-interview/qb_meta_<group>.json`: `{"<slug>": {"title": "<中文题名>", "requires": [<2–5 concept leaf ids
from concept_index.md that are free and of kind concept>]}}`.

## Gate (before replying)

`uv run python scripts/plain_style.py <your bodies>` ok, `python3 scripts/phone_diagrams.py vault/interviews/core/design-questions`
ok, `python3 -B scripts/check_wikilinks.py | tail -1` shows no dead link of yours. Then
`uv run python research/hello-interview/gen_skeleton.py && uv run trellis --domain hello-interview validate` — errors
may remain only for other groups' questions. Reply in ≤ 6 lines.
