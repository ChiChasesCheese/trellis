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

**How it reads (Chi, 2026-11-16: "说人话 … 能用卡片结构表达的东西就别一直复述 … 直接把题目或者说内容列出来").**
Show the content itself, laid out; never talk about it.

- No meta sentences: no 「本节介绍了」「这一部分讲的是」「我们需要注意」「值得一提的是」「下面我们来看」. Start with the content.
- Let the layout carry the structure: a table for things with the same fields (files, errors, examples), a numbered
  list for rules and steps, a code block for code and example calls with their output, a bold label in front of a
  short line. A paragraph only for the story card, and short.
- Say each thing once. Do not restate in prose what a table or code block already shows.
- Plain, spoken Chinese, like a colleague briefing you: 「坏在哪」「你要交什么」「给你的东西」, not textbook phrasing.
- Example of the wrong way: 「本章节主要介绍了返回值的约定，我们需要注意 remaining 的计算时机。」
  The right way:

  ```
  **返回** `(allowed, remaining, reset_after_ms)`

  | 字段 | 规则 |
  |---|---|
  | `remaining` | 本次判定之后还能放几次；被拒时为 0 |
  | `reset_after_ms` | 整数毫秒，向 0 截断 |
  ```

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

## Defects verifiers found (each is a rule)

- The story card leaves out README's run line (Python version, stdlib only, how to run, the port).
- A code block "quoted" with its docstring or `super().__init__` dropped is not verbatim.
- An order or choice README leaves open (which error wins when two apply, how long keys are kept) is written as the
  contract: say 「README 没规定」 and label ours 「本实现」.
- REFLECTION "good answer" bullets read like an official key: label them 「自拟要点，工作区文件里没有标准答案」.
- A test described more strongly than it asserts (`assertEqual` is 相等, not 同一个对象), or a rule called untested
  when one test does check it.
- A starter-defect row that was not run, a wrong row (the starter did snapshot; the defect was validating one pass and
  copying in a second), or a vague 「其他」 row.
- Tables with long sentences or unbreakable code in cells, or more than 3 columns: they overflow a phone.
- A cloze whose answer sits next to the blank; a `more` line with a fact found in no file (「8–10 分钟」).
- A code block labelled 「原样」 that stops partway: label it 「前 N 行」 or 「节选」 and say in one line what the rest does.
- A claim about what a value becomes on its way in (「缺字段或类型错都变成 `None`」) that was read, not run: run the
  adapter with a recording stub; wrong types often pass through unchanged.
- An example whose answer depends on data the stem leaves out (「两对内容不同」): put it in the stem.
- A rule credited to our reference that README actually states (「拒绝前导 + 和 0，接受 -0」): grep README before
  writing 「本实现」; the source column must be right both ways.
- An example input that a second rule masks (day 30 hides the extra-field defect): pick inputs where only the rule in
  question fires, and run them.
- A recall card asks about an open choice or rule no reading card states: every recall answer must be on a reading card.
- A count in prose that disagrees with the table under it (「三种结果」 over two rows).
