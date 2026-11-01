# Daily LeetCode deck — what the daily session does

Domain `leetcode-daily`, deck `LeetCode Tops::28 Daily（每日刷题）`. Chi (2026-10-31): every problem he solves on
LeetCode becomes one card, so that years later he can pick up the core idea again without the original context.

## Steps (one session per day; stop early when there is nothing new)

1. `cd /Users/chiserver/sessions/trellis && git pull -q --rebase`.
2. `uv run python scripts/leetcode_daily.py fetch` (new accepted problems → leaves in `skeleton/leetcode-daily.yaml`,
   statements in `sources/local/leetcode-daily/<slug>.txt`). Then `uv run python scripts/leetcode_daily.py pending`.
   If nothing is pending, stop (no commit, no push).
3. Write one card per pending leaf (rules below). More than 6 pending: split the leaves among up to 3 `sonnet`
   subagents, each told to read this file; otherwise write them yourself.
4. Gate: `uv run python research/companies/tiktok/tools/gate_cards.py vault/interviews/core/leetcode/daily/cards/*/*.md`
   (0 problems), `uv run python scripts/plain_style.py <new cards>` ok, `uv run trellis --domain leetcode-daily validate`
   0 errors.
5. `uv run trellis --domain leetcode-daily anki-push` (desktop Anki must be running; if AnkiConnect does not answer,
   skip this step and say so — the next run pushes).
6. Commit only `skeleton/leetcode-daily.yaml` and `vault/interviews/core/leetcode/daily/`, message
   `Daily LeetCode deck: <n> card(s) (<dates>)`, then
   `git pull -q --rebase && git push -q git@github.com:ChiChasesCheese/trellis.git HEAD:main`. `git checkout uv.lock`
   if uv touched it. Never commit `sources/local/`.

## The card

File `vault/interviews/core/leetcode/daily/cards/<month>/tlc-daily-<slug>-0-whole.md` (month = the leaf id before the
dot), frontmatter `id: tlc-daily-<slug>-0-whole`, `node: <leaf id>`, `type: qa`, no `step:`. Shape and every rule
follow the TikTok whole-answer cards: read `research/companies/tiktok/CARDS.md` (recursion first; 2-D DP as a full
table; comments carry the explanation; "What 简单解法 is") and copy the shape of
`vault/interviews/core/leetcode/tiktok/cards/p2/tlc-cheapest-flights-within-k-stops-0-whole.md`.

- Front: `**LC n 中文名**｜<Easy|Medium|Hard> · <solved date> 解出`, the full statement in Chinese with all constraints
  (copied from the statement file; translate faithfully when it is English) and 1–2 examples, then
  「给出完整的最优解答：考点、识别、推导、代码、复杂度、易错点。」
- Back, in order: **考点** (one or two lines: the core concept the problem tests, named so it can be searched, e.g.
  「贪心 + 交换论证」「状压 DP」「数位 DP」「并查集按值合并」) · **一句话** · **识别** (which statement signals point to it) ·
  **推导** (short: the obvious approach, why it fails, the key insight) · optional **简单解法** (only per CARDS.md) · the
  solution in one ```python block with Chinese comments carrying the reasoning · **运行** (real outputs on the
  examples) · **复杂度** · **易错点** (2–3, with a concrete wrong output where possible) · **同模式** (2–4 related LC
  problems, preferring ones in Chi's decks).
- Contest problems (often new, with no editorial): reason the solution out carefully; check it against a brute force on
  ≥ 300 random small inputs in `/tmp/daily_<slug>/` before writing outputs on the card. Never write the testing process
  on the card. Chinese prose, English terms in parentheses.
