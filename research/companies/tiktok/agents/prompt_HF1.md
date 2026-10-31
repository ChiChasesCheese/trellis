# Revise agent — TikTok pattern cards: add high-frequency examples, remove nothing (group H1)

Repo `/Users/chiserver/sessions/trellis`, branch `main`. Never commit, never spawn agents, edit only your files. Scratch
in `/tmp/hf_H1/`. `git checkout uv.lock` whenever uv touches it. Card rules: `research/companies/tiktok/CARDS.md`.

**Your cards** (in `vault/interviews/core/leetcode/tiktok/cards/patterns/`): tlc-patterns-backtracking-1-signals.md, tlc-patterns-binary-search-1-signals.md, tlc-patterns-design-9-problems.md, tlc-patterns-dp-knapsack-1-signals.md, tlc-patterns-dp-linear-8-problems.md, tlc-patterns-greedy-1-signals.md, tlc-patterns-hashing-5-variants.md, tlc-patterns-heap-patterns-5-variants.md, tlc-patterns-intervals-sweep-5-variants.md, tlc-patterns-linked-list-5-more-variants.md, tlc-patterns-math-bit-sim-9-problems.md, tlc-patterns-monotonic-stack-7-problems.md, tlc-patterns-prefix-sum-7-problems.md, tlc-patterns-signals-4-near-miss.md, tlc-patterns-sliding-window-7-problems.md, tlc-patterns-topo-sort-1-signals.md, tlc-patterns-tree-bfs-bst-1-signals.md, tlc-patterns-tree-dfs-1-signals.md, tlc-patterns-trie-1-signals.md, tlc-patterns-two-pointers-5-variants.md, tlc-patterns-union-find-6-variants.md

Chi (2026-10-31): only 44 % of the folded examples on the pattern cards are TikTok high-frequency problems (bands
P1–P4); half come from tier B. He wants more high-frequency problems **added — nothing removed**.

The high-frequency problems with their LeetCode tags: `sources/local/tiktok-high-freq.json` (band p1 is the most
frequent). Their full solutions: `vault/interviews/core/leetcode/tiktok/cards/*/tlc-<slug>-0-whole.md`.

For each card:
1. Signal / near-miss / variant cards: for every bullet whose example is not in bands p1–p4, look for a p1–p4 problem
   that shows the same signal truly well. If one exists, add it to the bullet as 「（例：LC a 旧题；高频：LC b 新题）」 and
   append a folded block for it after the existing blocks of that card. Skip when nothing fits well; never force it.
2. Problem-list cards: inside each variant group, append the p1–p4 problems that clearly belong to that variant and are
   not listed yet (mark them 「（高频）」), and append a folded block for each, after the existing blocks.
3. Block shape as already used on the card: `**例题：** LC n 名字`, one or two sentences of statement, the main solution
   from that problem's whole card (comments / blank lines may go, logic unchanged; recursion-first and full-table rules
   already hold there). Verify each new block on the problem's first example in a scratch harness.
4. Never delete or rewrite existing examples or bullets beyond adding the new problem name.

Gate: `uv run python research/companies/tiktok/tools/gate_cards.py <your files>` (0 problems),
`uv run python scripts/plain_style.py <your files>` ok, `uv run trellis --domain tiktok-lc validate` 0 errors.

Reply (≤ 6 lines): blocks added, distinct high-frequency problems added, cards with nothing added and why.
