# Course card agent — Hello Interview chapters as summary + question cards

Repo `/Users/chiserver/sessions/trellis`. Never commit, never spawn agents, write only your pages' files. Scratch in
`/tmp/hc_<group>/`. `git checkout uv.lock` whenever uv touches it. **Resume rule:** run the checker first (below) and skip
every page it reports `ok`.

Chi (2026-11-03) is a senior candidate who wants each chapter of Hello Interview's system design and low-level design
courses turned into cards: what the chapter says, how it is tested, and what a senior should know beyond it. Nothing may
be missed, and every card must be useful on its own months later on a phone.

## Input

Your group file lists pages as `<leaf> <stem>`. Page text: `sources/local/hello-interview/premium/pages/<stem>.md`. Read all
of it first. Existing cards for the page (do not repeat them, build around them):
`grep -rl "^node: .*<page>" vault/domains/hello-interview/cards --include=*.md` and `research/hello-interview/concept_home.json`.

## Three kinds of cards, one leaf each

Folder `vault/domains/hello-interview/cards/premium/<sd|lld>/<section>/<page>/`, one file per card. This folder is gitignored
and never reaches the public repo. Frontmatter exactly:

```
---
id: hi-c-<sd|lld>-<page>-<n|x|b><NN>-<short-slug>
node: <leaf>.<notes|exam|beyond>
type: qa
step: <NN>
---
```

`<page>` is the last part of the leaf. `NN` restarts at 01 per kind. In each kind, 必会 first, then 追问, then 加分.

1. **摘要 (`notes`, `n`).** One card per section of the page, following its order. A long section with distinct sub-topics gets one
   card per sub-topic. Front: what the section answers, as a real question a reader understands with no page open. Back: the
   section's content in tight bullets, keeping every mechanism, number, option and trade-off that matters. Header
   `**<章名> · <小节>**｜摘要 · 必会` (or 追问 / 加分 for side material).
2. **考点 (`exam`, `x`).** How the chapter gets tested: apply it to a scenario, choose between options the page weighs, predict
   a failure, spot the mistake, say what a senior adds over a mid-level answer. Not a rephrased summary. Fill what the
   existing cards miss; together about 6–10 for a concept page, 8–12 for a problem breakdown, 3–5 for a short overview.
   Header `**<章名> · <要点>**｜考点 · 必会`.
3. **拓展 (`beyond`, `b`).** What a senior interviewer pushes on that the page does not cover: production failure modes,
   operating at scale, real system behaviour, a newer alternative, the deeper why. 2–5 per page, 0–1 for a short overview.
   Only well-established facts that you are sure of; never an invented number. Header `**<章名> · <要点>**｜拓展 · 加分` (or 追问).

For a **problem breakdown**, the first summary card (`n01`) is the whole answer on one card: a `**60 分钟路线。**` table, then the requirements, entities and API, overall design, deep dives and level expectations as nested bullets (they fold in Anki), about 800–1500 Chinese characters. Same format as
`vault/interviews/core/design-questions/payment-batch-processing.md`, and for low-level design `kv-store-eviction.md` (core code about 90 lines at most). The remaining summary cards follow the delivery steps: requirements with numbers, entities and API, the
high-level flow, then one card per deep dive (the problem, each option with its flaw, the choice and why), then what is
expected at each level. Respect 60 minutes: tag what a candidate must say as 必会 and what comes only on follow-up as 追问 or 加分.

For **low-level design**, code is short Python 3 with type hints. Comments carry the reasoning; prose never repeats the code. Write
your own code rather than porting the page's. Run every snippet longer than 5 lines in your scratch folder before keeping it.
Keep the concurrency claims precise (what the lock protects, what breaks without it).

**Chi's goal (2026-11-03) is much stronger core coding and deeper Python.** In the 拓展 cards of every low-level design page, include 1-3 cards on the advanced Python or the architecture reasoning behind the chapter's code: what the idiom does underneath, what the plainer version costs, when not to use it. Run the snippets. On any page, name the general pattern where one applies, as `**模式。**` with a short name such as 转换表状态机 or 注入时钟.

## Style

- Chinese, technical terms in English in parentheses on first use. Back about 100–250 Chinese characters (except the whole-answer card); bullets and small tables
  over paragraphs; phone width. Nested bullets fold in Anki, so put the takeaway in the parent bullet.
- **Teach, do not list (Chi says his fundamentals are weak).** A bullet is a sentence a reader understands alone, with its reason: not "顺序就是常见程度" but why the simplest option comes first and what signal moves you to the next one. A table's rows say when and why. A summary card with fewer than about 100 Chinese characters is almost always too thin; introduce each term where it first appears.
- **Your own words.** Facts, numbers and design choices are fine; never copy or closely paraphrase sentences, and never lift the
  page's examples word for word.
- Self-contained: no 页面, 原文, 本章, 这一章, 这一节, 课程, 上面, 前面提到, no site name, no URL, no citation, no process talk. `check_course.py` rejects these.
- The style checker rejects 这道题, 本题, 本书, 抓取 and 面经 (even inside 页面经常).

## Coverage ledger

For each page write `sources/local/hello-interview/premium/coverage/<stem>.json`:

```json
{"sections": {"<exact heading text from the page>": ["<card id>", "..."], "<heading>": "skip: <why, e.g. video link, closing line>"}}
```

Every `##` and every substantial `###` heading must appear. A skip is only for material with nothing to learn.

## Gate, before replying

```
uv run python research/hello-interview/check_course.py --group <group file>
uv run python scripts/plain_style.py <your card files>
python3 scripts/phone_diagrams.py vault/domains/hello-interview/cards/premium/<...>
uv run trellis --domain hello-interview validate
```

Everything green, 0 validate errors, and no `not_self_contained` / `leans_on_source` on your cards. Reply in ≤ 6 lines: pages done, cards by
kind, snippets run, and the 拓展 claims you are least sure of.
