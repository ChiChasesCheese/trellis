# Revise agent — TikTok pattern cards: one problem per signal, folded short code (group S1)

Repo `/Users/chiserver/sessions/trellis`, branch `main`. Never commit, never spawn agents, edit only your files. Scratch
in `/tmp/sig_S1/`. `git checkout uv.lock` whenever uv touches it. Card style rules: `research/companies/tiktok/CARDS.md`
(Chinese, recursion first, 2-D DP as full tables, main problem first).

**Your cards** (in `vault/interviews/core/leetcode/tiktok/cards/patterns/`): tlc-patterns-backtracking-1-signals.md, tlc-patterns-design-1-signals.md, tlc-patterns-dp-linear-1-signals.md, tlc-patterns-hashing-1-signals.md, tlc-patterns-heap-patterns-5-variants.md, tlc-patterns-linked-list-1-signals.md, tlc-patterns-monotonic-stack-1-signals.md, tlc-patterns-prefix-sum-5-variants.md, tlc-patterns-sliding-window-1-signals.md, tlc-patterns-topo-sort-1-signals.md, tlc-patterns-tree-bfs-bst-5-variants.md, tlc-patterns-trie-1-signals.md, tlc-patterns-union-find-1-signals.md

Chi (2026-10-30), reading the prefix-sum signals card: every signal should come with a problem, and the short code
answer should sit under the card, folded, ready to expand; map to TikTok problems as much as possible.

For each card:
1. Every bullet that names a signal, a near-miss or a variant gets **one** problem: append 「（例：LC n 中文名）」 to the
   bullet. Pick from the TikTok deck first (`research/companies/tiktok/index.json`; prefer `band` p1..p4, then `b`),
   else from Chi's other decks (`sources/local/lc-in-decks.json`). A bullet that already names a problem keeps it if
   that problem is in the TikTok deck, otherwise swap it for a TikTok one that shows the same signal.
2. At the end of the card, one folded block per problem, in bullet order, exactly this shape (the template folds every
   `**例题：**` block separately):

   **例题：** LC 560 和为 K 的子数组

   一两句题意（含关键约束）。

   ```python
   <short solution: the main solution of that problem's whole-answer card in
    vault/interviews/core/leetcode/tiktok/cards/*/tlc-<slug>-0-whole.md, ≤ 15 lines; you may drop comments or
    blank lines but must not change the logic>
   ```

3. Remove an old trailing `**对应 LeetCode：**` / `**同模式**` line if the examples now cover it.
4. Verify every code block you add runs on the problem's first example (write a tiny harness in scratch).

Gate: `uv run python research/companies/tiktok/tools/gate_cards.py <your files>` (0 problems),
`uv run python scripts/plain_style.py <your files>` ok, `uv run trellis --domain tiktok-lc validate` 0 errors
(long-answer warnings on these cards are expected).

Reply (≤ 8 lines): cards done, problems used (count TikTok vs other decks), bullets left without a problem and why.
