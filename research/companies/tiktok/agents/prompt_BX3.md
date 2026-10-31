# Revise agent — TikTok pattern cards: drop tier-B examples that are on no other list (group X3)

Repo `/Users/chiserver/sessions/trellis`, branch `main`. Never commit, never spawn agents, edit only your files. Scratch
in `/tmp/bx_X3/`. `git checkout uv.lock` whenever uv touches it. Card rules: `research/companies/tiktok/CARDS.md`.

Chi (2026-10-31): an example from TikTok tier B may stay on a pattern card **only if the problem is also on another
list** — Chi's Amazon or topic decks, Blind 75, NeetCode 150, LeetCode Hot 100 or Top Interview 150
(`research/companies/tiktok/catalog/other_lists.json`). Tier-A problems (`band` p1–p4 in
`research/companies/tiktok/index.json`) always qualify.

**Your cards and the problems to drop from each** (cards in `vault/interviews/core/leetcode/tiktok/cards/patterns/`):
- tlc-patterns-backtracking-8-problems.md: LC 47, LC 473
- tlc-patterns-design-1-signals.md: LC 1146, LC 1381
- tlc-patterns-dp-grid-string-9-problems.md: LC 2850, LC 3389, LC 3441
- tlc-patterns-dp-linear-1-signals.md: LC 714
- tlc-patterns-graph-traversal-8-problems.md: LC 317, LC 924, LC 934, LC 1466
- tlc-patterns-hashing-1-signals.md: LC 523, LC 593
- tlc-patterns-heap-patterns-5-variants.md: LC 2402
- tlc-patterns-intervals-sweep-5-variants.md: LC 2021
- tlc-patterns-linked-list-5-more-variants.md: LC 1171
- tlc-patterns-math-bit-sim-9-problems.md: LC 442, LC 670, LC 1071, LC 1860, LC 2523
- tlc-patterns-prefix-sum-1-signals.md: LC 1074, LC 2021
- tlc-patterns-shortest-path-1-signals.md: LC 499, LC 1129, LC 1462
- tlc-patterns-sliding-window-1-signals.md: LC 1151
- tlc-patterns-string-parsing-1-signals.md: LC 165, LC 187, LC 1249
- tlc-patterns-topo-sort-6-variants.md: LC 1462
- tlc-patterns-tree-bfs-bst-7-problems.md: LC 426
- tlc-patterns-tree-dfs-7-problems.md: LC 298, LC 426, LC 1530
- tlc-patterns-two-pointers-1-signals.md: LC 939
- tlc-patterns-union-find-1-signals.md: LC 1466

For each listed problem on a card:
1. If the same bullet / list group already has another example that qualifies (often a 「高频：LC …」 added earlier),
   remove the dropped problem: its mention in the bullet and its folded `**例题：**` block.
2. Otherwise look for a qualifying replacement that shows the same signal truly well: first tier A
   (`sources/local/tiktok-high-freq.json`, code in the whole cards), then the other lists (code in
   `sources/local/lc-in-decks.json`). Put it in the bullet / list in place of the dropped one and replace the folded
   block (one or two sentences + the main solution, verified on the first example in a scratch harness).
3. If nothing qualifies, remove the dropped problem and its block; the bullet stays without an example (on list cards,
   drop the entry; drop a group heading that ends up empty).
Keep everything else unchanged.

Gate: `uv run python research/companies/tiktok/tools/gate_cards.py <your files>` (0 problems),
`uv run python scripts/plain_style.py <your files>` ok, `uv run trellis --domain tiktok-lc validate` 0 errors. Then
confirm no remaining 例题 on your cards is tier B without another list.

Reply (≤ 6 lines): problems dropped, replaced (with what), and bullets left without an example.
