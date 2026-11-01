# Daily LeetCode deck — what the daily session does

Domain `leetcode-daily`, deck `LeetCode Tops::28 Daily（按知识点）`, one sub-deck per knowledge point. Chi (2026-10-31): every problem he solves on
LeetCode becomes one card, so that years later he can pick up the core idea again without the original context.

## Steps (one session per day; stop early when there is nothing new)

1. `cd /Users/chiserver/sessions/trellis && git pull -q --rebase`.
2. `uv run python scripts/leetcode_daily.py fetch` (new accepted problems → leaves in `skeleton/leetcode-daily.yaml`,
   statements in `sources/local/leetcode-daily/<slug>.txt`). Then `uv run python scripts/leetcode_daily.py pending`.
   If nothing is pending, stop (no commit, no push).
3. For each pending leaf whose shared body `vault/interviews/core/leetcode/problems/<slug>.md` already exists (another
   deck wrote it), only file it (below). Otherwise write the body (rules below) to that path, then file it:
   `uv run python scripts/leetcode_daily.py place <slug> <point-id>` (`points` lists them; they are the TikTok deck's
   pattern branches). When none fits, open a new one: `place <slug> <new-id> "中文标题"` (Chi, 2026-10-31: sub-decks are
   knowledge points or new groups, never dates). Nothing may stay in `inbox`. More than 6 pending: split the leaves among up to 3 `sonnet`
   subagents, each told to read this file; otherwise write them yourself.
4. Gate: `python3 scripts/check_daily_refs.py` (every printed line is a wrong LC number or name; fix it), `uv run python research/companies/tiktok/tools/gate_cards.py vault/interviews/core/leetcode/problems/<new slugs>.md`
   (0 problems), `uv run python scripts/plain_style.py <new cards>` ok, `uv run trellis --domain leetcode-daily validate`
   0 errors.
5. `uv run trellis --domain leetcode-daily anki-push` (desktop Anki must be running; if AnkiConnect does not answer,
   skip this step and say so — the next run pushes).
6. Commit only `skeleton/leetcode-daily.yaml`, `vault/interviews/core/leetcode/daily/` and the new files in `vault/interviews/core/leetcode/problems/`, message
   `Daily LeetCode deck: <n> card(s)`, then
   `git pull -q --rebase && git push -q git@github.com:ChiChasesCheese/trellis.git HEAD:main`. `git checkout uv.lock`
   if uv touched it. Never commit `sources/local/`.

## Every run, last step (even when nothing was pending)

`uv run python scripts/lc_mustread.py` rebuilds `LeetCode Tops::00 必读（每天自动更新）` from Chi's latest Anki history and
recent solves, pushes it and drops what left the list. Its files are gitignored (personal stats); never commit them.

## The card

One body per problem, shared by every deck (Chi, 2026-11-01): write `vault/interviews/core/leetcode/problems/<slug>.md`
with frontmatter `slug: <slug>` only. `place` then writes this deck's stub
`vault/interviews/core/leetcode/daily/cards/tlc-daily-<slug>-0-whole.md` (id, node, `body:`, `meta:`); never copy a
body into a deck folder, and improve an existing body in place instead of writing a second one. Shape and every rule
follow the TikTok whole-answer cards: read `research/companies/tiktok/CARDS.md` (recursion first; 2-D DP as a full
table; comments carry the explanation; "What 简单解法 is") and copy the shape of
`vault/interviews/core/leetcode/tiktok/cards/p2/tlc-cheapest-flights-within-k-stops-0-whole.md`.

- Front: `**LC n 中文名**｜<Easy|Medium|Hard>` (decks add their own facts after ｜ through `meta:`; no solve date, no 「每日」 wording anywhere on the card), the full statement in Chinese with all constraints
  (copied from the statement file; translate faithfully when it is English) and 1–2 examples, then
  「给出完整的最优解答：考点、识别、推导、代码、复杂度、易错点。」
- Back, in order: **考点** (one or two lines: the core concept the problem tests, named so it can be searched, e.g.
  「贪心 + 交换论证」「状压 DP」「数位 DP」「并查集按值合并」) · **核心题** (see below) · **一句话** · **识别** (which statement signals point to it) ·
  **推导** (short: the obvious approach, why it fails, the key insight) · optional **简单解法** (only per CARDS.md) · the
  solution in one ```python block with Chinese comments carrying the reasoning · **运行** (real outputs on the
  examples) · **复杂度** · **易错点** (2–3, with a concrete wrong output where possible) · **同模式** (2–4 related LC
  problems, preferring ones in Chi's decks).
- Contest problems (often new, with no editorial): reason the solution out carefully; check it against a brute force on
  ≥ 300 random small inputs in `/tmp/daily_<slug>/` before writing outputs on the card. Never write the testing process
  on the card. Chinese prose, English terms in parentheses.

## 核心题 (Chi, 2026-10-31): map every problem back to the canonical problem of its knowledge point

"我们最好每个题都 map 回对应知识点的核心题，最好在几个 top list 里面". Right after **考点**, write:

```
**核心题。**

- LC n 中文名（Blind 75、Hot 100）：一句话说清本题和它的关系（同一个模型 / 本题多了什么 / 换了什么）
```

One bullet per knowledge point in 考点 (usually 1, at most 2). Pick the problem from Blind 75 / NeetCode 150 / LeetCode
Hot 100 / Top Interview 150 that is the textbook problem of that point, preferring the one on more lists:
`python3 scripts/core_lists.py <tag or word>` lists them with tags and lists (copy the name from there). Only when no
list problem teaches the point, take the classic problem from Chi's TikTok deck and write 「（不在题单）」 instead of the
list names. The bullet must start with `LC n` (the deck opens it in place); keep the relation to one clause without
commas, or use 「：」 then a short sentence. Never the problem itself.
