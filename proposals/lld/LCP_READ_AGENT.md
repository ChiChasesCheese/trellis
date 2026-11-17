# LeetCode Project: 题目 (reading cards) and 题目理解 (recall cards) — writer and verifier

Chi (2026-11-16) opened the ten-second cards and could not place them: "我对这些题没有概念，不知道前因后果，你直接给我
细节的东西我没有办法掌握". Before any detail, each project now starts with **题目**: reading cards, one per workspace file
(or one part of a long file), that he reads to understand the project — the story, the contract, the code he is given.
After them comes **题目理解**: short recall questions on the problem itself, so he checks that he can bring the key facts
back without the files. Only then the existing ten-second cards and synthesis cards.

Repository root: `/Users/chiserver/sessions/trellis`. Everything here is local and private (the cards restate and quote
LeetCode Premium files): write only under `sources/local/lc-project/quick/`. No git, no other agents.

## Input, for project `<slug>`

- `sources/local/lc-project/workspaces/<slug>/files/`: the whole workspace — README.md, OVERVIEW.md, the template(s),
  provided modules (models, server, app, db, migrations, ops scripts), public tests, REFLECTION.essay. Read every file.
- `vault/domains/low-level-design/problems/lcp-<slug>/solution.py` (our reference) and the article
  `readings/problems/solution-lcp-<slug>.md`: to check that every number and rule you state is right.
- `sources/local/lc-project/quick/points/<slug>.json` and `cards/<slug>.jsonl`: the existing points and cards. **Keep
  them**; you add to them.

## Output

Insert your points **at the start** of `points/<slug>.json` (reading points first, then recall points, then the existing
points unchanged), and append your cards to `cards/<slug>.jsonl`. Points: `{"kp": "<slug>.<name>", "title": "<中文>",
"kind": "file" | "recall", "leaves": ["lcproject.lcp-<slug>", …]}` (add real LLD leaf ids where a recall point is
about a concept). Cards carry `based_on` from `readme`, `overview`, `template`, `tests`, `reflection`, `solution`,
`article`.

## 题目: reading cards (`fmt: "read"`, kind `file`)

A reading card has `title`, `body` (markdown: short paragraphs, bullets, tables, ```python code blocks```), `key` (one
line ≤ 60 units: the takeaway). It is read once, then graded understood / not; it is not a ten-second card, but it must
be readable in one to two minutes: prose ≤ 900 units, code ≤ 40 lines (`uv run python scripts/lcp_quick.py gate <slug>`
checks). Chinese, plain, structured; terms engineers say in English stay English.

Write, in this order:

1. **题目背景与前因后果** — the story first: what the system is, who uses it, what is broken or missing and how that
   shows up (the symptoms), what you must deliver, what is given to you, how it is judged (hidden tests on submit,
   working with the coding agent, REFLECTION answers), the time limit. End with a table: every workspace file, one line
   on its role, and whether you edit it.
2. **One card per file** in the order a candidate should read them: README (split into 2–5 cards by section when long:
   场景 / 接口与返回 / 规则 / 示例 / 文件与运行), the template file (its classes and method signatures verbatim, what each
   must do, what is already provided), each provided module that matters (models, server/app, db, ops scripts — its role
   and the few lines you need to know), the public tests (what each checks, and what they do not check), REFLECTION
   (the questions, faithfully in Chinese, and what a strong answer covers in 2–3 bullets).
3. Quote the code that matters **verbatim** from the workspace (signatures, data classes, the example calls and their
   outputs, error tables). Restate rules faithfully: never add a rule the files do not state; where the files leave a
   choice open, say so ("README 没规定").
4. Every number and example output you show is checked by running our solution (or the workspace example) — state only
   what you ran.

Expect 5–10 reading cards per project.

## 题目理解: recall cards (kind `recall`)

8–15 ten-second cards in the usual quick formats (`mc`, `judge`, `order`, `cloze`, `match`, `multi`; mostly tapped), each
with `more`, all answerable from the reading cards alone and testing the problem itself: what you implement and its
signature, the return shape, the key rules and their order, the numbers in the README examples, which files you may edit,
what the public tests do not cover, the symptoms of a repair project, the REFLECTION topics. Follow
`proposals/lld/LCP_QUICK_AGENT.md` for these cards (limits, one answer, real distractors, its "Defects verifiers found").
Do not repeat a point the existing quick cards already test; recall cards are about knowing the problem, the existing
cards about solving it.

## Steps (writer)

1. Resume rule: if `points/<slug>.json` already starts with `file` points, write only what is missing.
2. Read every workspace file, then write the points and cards (a Python script that edits the JSON, `ensure_ascii`
   off). Run `uv run python scripts/lcp_quick.py gate <slug>` until it reports 0 failing and 0 without a card.
3. Report per project: reading cards (titles), recall cards per format, and the three statements you are least sure
   are faithful to the files.

## Steps (verifier)

You did not write these cards. For each `file` and `recall` card of `<slug>`, open the workspace files and judge:
**faithful** (every rule, signature, number and example matches the files; nothing invented; open choices marked open),
**complete** (the story card and the file cards together cover every README section and every file a candidate needs),
**readable** (structured, plain Chinese, no wall of text, code blocks verbatim), and for recall cards the usual quick-card
checks. Append one verdict line per card to `sources/local/lc-project/quick/verify/<slug>.jsonl` (`ok` / `fix` with the
whole corrected card / `drop`), keep the existing lines, run the gate, and report counts and fixes.
