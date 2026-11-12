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
body into a deck folder, and improve an existing body in place instead of writing a second one. Chi memorises
patterns (2026-11-11): every card is short. Copy the shape of
`vault/interviews/core/leetcode/problems/rotting-oranges.md` exactly.

- Front: `**LC n 中文名**｜<Easy|Medium|Hard>`, then the statement in one or two lines (what is given, what is asked; a
  constraint only if the solution depends on it). No example list, no solve date, no 「每日」 wording.
- Back, in order:
  - **一句话**: one sentence naming the pattern and the key move.
  - The main solution in one ```python block: no imports, no type hints, at most 60 characters per line, a few short
    comments. Tree and graph DFS are recursive; a 2-D DP keeps the full table.
  - **复杂度**: one line, `时间 …，空间 …。`
  - **易错点**: 1–3 real bugs, each `<短语>：<一句>`.
  - **追问**: 1–3 bullets, each `<问题？>：<一两句答案>` (the card folds the answer).
  - **同模式**: at most 4 `LC n 标题` separated by 、. The first is the textbook problem of this knowledge point from
    Blind 75 / NeetCode 150 / Hot 100 / Top Interview 150 (`python3 scripts/core_lists.py <tag or word>`); the card
    expands each into that problem's own code.
- No 考点, 核心题, 识别, 推导, 运行 or 拓展优化 sections.
- Contest problems (often new, with no editorial): reason the solution out carefully; check it against a brute force on
  ≥ 300 random small inputs in `/tmp/daily_<slug>/`. Never write the testing process on the card. Chinese prose,
  English terms in parentheses only when they help recall.

