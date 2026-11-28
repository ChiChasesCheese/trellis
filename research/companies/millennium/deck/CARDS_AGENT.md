# Millennium cards — writer's brief

Chi interviews for **Millennium, Software Engineer – Learning Engineering and Data (LEaD) Program, Miami**. He passed
the first round (45-minute live coding, 5 October). Next: a 30-minute recruiter call (Monday 30 November), then a team
round of several interviews whose format is not known yet. He will study this deck in about 15 hours over two days, so
every card must earn its place: what he needs to say, know or code in those rounds, nothing else.

Work in `/Users/chiserver/sessions/trellis`. Local files only: no web, no git, no Anki, no subagents. Card by card:
read the sources, think, write one card, then the next; never script the batch.

## Where things are

- Skeleton (the leaves you write under): `skeleton/millennium.yaml`. Read it first; every card's `node:` is one of its
  ids. Write only under the branches your task names.
- Cards: `vault/interviews/companies/millennium/deck/cards/<branch>/<id>.md`.
- Sources (the kit, written in September): `vault/interviews/companies/millennium/` — `01-company-brief.md`,
  `02-process.md`, `fit.md`, `06-questions-to-ask.md`, `loop/LOOP_GUIDE.md`, `loop/rounds/*/questions.md`,
  `loop/rounds/05_hm_behavioral/stories.md`, `loop/rounds/01_first_round/pc*/` (`problem.md`, `solution.py`),
  `study/30-articles/pc*.md`, `loop/rounds/04_system_design/sd01_market_data_service/`, `study/20-cards/*.md`.
  Evidence behind the kit: `research/companies/millennium/catalog/` (CATALOG.md and raw/).
- Chi's interview stories (his own work, already written for interviews): `vault/interviews/core/stories/S1 … S11*.md`,
  spoken in the format of `vault/interviews/core/stories/SPOKEN_FORMAT.md`. His resume: `vault/interviews/core/resume/`.

## Card file

```
---
id: mlp-<branch>-<short-name>
node: <leaf id from the skeleton>
type: qa
step: <1, 2, 3 … within the leaf, in reading order>
---
## Q
**<短标题>**｜<分支名，如 招聘方电话>

<the question, as the interviewer or the situation would put it>

## A
…
```

Every branch also gets **one map card on the branch node itself** (`node: call`, id `mlp-<branch>-0-map`, step 0):
`**一句话。**` what this part is for; one diagram (rules below) showing its blocks; `**关键直觉。**` 2–4 bullets, the
ideas that tie the part together. Nothing under the diagram repeats it.

## How the answer is written

- **Self-contained and textbook-plain.** Chi is assumed to know nothing about Millennium or finance. Every term the card
  uses is explained in a few words where it first appears (English term in parentheses once). Each card stands alone.
- **Content, not talk.** Chinese prose, short bold-phrase bullets (`- **短语：** 一两句`), one line each. No sentence
  about the card, the sources, the kit or the reader. No tables (they do not fit a phone). No headings inside the answer.
- **What he says out loud is English.** Any answer he gives in an interview has a block `**英文答法。**` with 2–6 short
  spoken lines in first person, the way he would actually say them (not an essay); key words in bold. Chinese bullets
  around it explain why that answer and what the interviewer is checking.
- **Diagrams where they explain** (a flow, a structure, a timeline): mermaid only.
  - Who does what in order → `sequenceDiagram`, first line exactly
    `%%{init: {"sequence": {"mirrorActors": false}}}%%`, at most 4 participants, at most 8 messages, each label ≤ 10 字.
  - A structure → `flowchart LR`, first line exactly
    `%%{init: {"flowchart": {"wrappingWidth": 320}, "themeVariables": {"fontSize": "18px"}}}%%`, at most three columns,
    at most 12 boxes, labels ≤ 10 字, every label quoted `A["…"]`.
  - Never a left-to-right chain of four or more boxes. What the diagram shows is not said again in words.
- **Length:** 200–550 汉字 of prose per card (diagram and code do not count).
- **Facts only from the sources.** Numbers, names, dates exactly as the sources give them. Never write a person's name
  (interviewers, recruiters) on a card. **No annotations of any kind** (Chi: 「不要加任何注释注解：不一致、需要核对等等和学习
  本身没关系的东西」): no 「（推断）」, 「待确认」, 「未验证」, 「来源」, 「面经说」, no confidence labels, no remark that sources
  disagree. When something is uncertain, leave it out. General knowledge (what a hedge fund is, how a hash map works)
  is written plainly and must be true in general.

## Coding cards (branch `coding`)

Two cards per problem, from `problem.md`, `solution.py` and `study/30-articles/pc*.md`:
1. `题与解` — the problem in 2–3 lines; `**一句话思路。**`; the solution as one Python code block (no imports unless
   needed, inline comments carry the explanation, the intuitive version first); `**复杂度。**`; then the 2–3 things to
   say out loud while coding (`**边写边讲。**` in English).
2. `追问与变体` — each follow-up the problem's later parts or the article raise: `- **<追问>：** 做法一句话`, with a short
   code block only where the change is not obvious; edge cases that cost a test case.

## Design cards (branch `design`)

From the four sd01 files: `这道题的地图` (requirements with numbers, entities, API, the high-level path), `高层设计`
(components and each path, one diagram), `深挖清单` (each deep dive: approach; why; cost), then one card per major
deep dive in the model answer (as-of queries, ingestion and corrections, fan-out to subscribers). Same rules as above.

## Gate

After each branch: `uv run trellis --domain millennium validate` must show 0 errors, and
`uv run python scripts/check_mermaid.py vault/interviews/companies/millennium/deck/cards/<branch>/*.md` must say every
diagram renders. Resume rule: a leaf that already has its cards is done; skip it.

## Report (final message, at most 10 lines)

Per branch: number of cards and one line on what they cover. Then any leaf you could not fill from the sources.
