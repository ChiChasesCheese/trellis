# Daily LeetCode — what the daily session does

Chi (2026-10-31): every problem he solves on LeetCode becomes a card, so that years later he can pick up the core idea
again. Since 2026-11-14 every problem has exactly **one** card, on its leaf of the LeetCode knowledge tree (domain
`leetcode-tree`, deck 算法知识树（灵神题单）, card id `lct-<slug>`); lists, companies, "solved" and "must-read" are tags
on that card (see `research/leetcode-unify/README.md`). `skeleton/leetcode-daily.yaml` stays only as the ledger of what
he solved; its deck is retired (`anki_via: leetcode-tree`), so never anki-push it.

## Steps (one session per day; stop early when there is nothing new)

1. `cd /Users/chiserver/sessions/trellis && git pull -q --rebase`.
2. `uv run python scripts/leetcode_daily.py fetch` (new accepted problems → the ledger, statements in
   `sources/local/leetcode-daily/<slug>.txt`). Then `uv run python scripts/leetcode_daily.py pending`.
   If nothing is pending, skip to the last step.
3. For each pending problem whose body `vault/interviews/core/leetcode/problems/<slug>.md` already exists, only file
   it (below). Otherwise write the body (rules below), then file it:
   `uv run python scripts/leetcode_daily.py place <slug> <point-id>` (this only records it in the ledger; `points`
   lists the ids, and `place <slug> <new-id> "中文标题"` opens one). Nothing may stay in `inbox`.
4. Put each new problem on the tree, following `research/leetcode-unify/PLACEMENT.md`:
   - run `uv run python scripts/lc_analysis.py`;
   - a problem on one of 0x3F's lists lands on its leaf by itself;
   - any other goes into `sources/local/lc/expand.json` under the best leaf, or a leaf of ours in
     `sources/local/lc/our_leaves.json`;
   - then run `uv run python scripts/lc_tree.py --write` and check that `vault/interviews/core/leetcode/tree/cards/**/lct-<slug>.md` exists.
5. Gate:
   - `python3 scripts/check_daily_refs.py` must print nothing;
   - `uv run python scripts/plain_style.py <new bodies>` must be ok;
   - `uv run trellis --domain leetcode-tree validate` and `uv run trellis --domain leetcode-tops validate` must show 0 errors (the second checks the shared bodies).
6. Anki (desktop Anki must be running; if AnkiConnect does not answer, skip this step and say so):
   - `uv run python scripts/anki_refresh.py --add lct- leetcode-tree` adds the new cards;
   - `uv run python scripts/lc_tags.py --apply` refreshes the list and company tags.
7. Commit only `skeleton/leetcode-daily.yaml` and the new files in `vault/interviews/core/leetcode/problems/`. The tree
   (skeleton and cards) is local. Use the message `Daily LeetCode: <n> problem(s)`, then
   `git pull -q --rebase && git push -q git@github.com:ChiChasesCheese/trellis.git HEAD:main`. Run `git checkout uv.lock`
   if uv touched it. Never commit `sources/local/`.

## Every run, last step (even when nothing was pending)

Run `uv run python scripts/lc_mustread.py`. It moves the tag `必读` onto the problems to review today, computed from Chi's
latest Anki history and recent solves.

## The card

One body per problem, shared by every deck (Chi, 2026-11-01): write `vault/interviews/core/leetcode/problems/<slug>.md`
with frontmatter `slug: <slug>` only. Its one card is the tree stub `lct-<slug>` that `lc_tree.py --write`
writes; never copy a body into a deck folder, and improve an existing body in place instead of writing a second one. Chi memorises
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

## Diagram baseline

- **Diagrams (Chi, 2026-11-13): at least 25% of a deck's cards carry one, aim for 30%.** A ```mermaid flowchart / sequenceDiagram / stateDiagram-v2 or a ```svg block wherever a flow, architecture, state machine, layout or comparison is the point. Render-check each mermaid; measure with `uv run python scripts/diagram_share.py <domain>` (exit 1 below 25%).
