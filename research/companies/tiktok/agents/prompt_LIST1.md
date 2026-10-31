# Revise agent — TikTok pattern cards: one problem per signal, folded short code (group L1)

Repo `/Users/chiserver/sessions/trellis`, branch `main`. Never commit, never spawn agents, edit only your files. Scratch
in `/tmp/sig_L1/`. `git checkout uv.lock` whenever uv touches it. Card style rules: `research/companies/tiktok/CARDS.md`
(Chinese, recursion first, 2-D DP as full tables, main problem first).

**Your cards** (in `vault/interviews/core/leetcode/tiktok/cards/patterns/`): tlc-patterns-backtracking-8-problems.md, tlc-patterns-dp-grid-string-9-problems.md, tlc-patterns-graph-traversal-8-problems.md, tlc-patterns-heap-patterns-7-problems.md, tlc-patterns-math-bit-sim-9-problems.md, tlc-patterns-shortest-path-7-problems.md, tlc-patterns-topo-sort-9-problems.md, tlc-patterns-trie-9-problems.md

These are the per-pattern **problem-list** cards (「本组用到 X 的题」, grouped by variant). Chi saw one and asked why it
still has no answers: every listed problem should come with its short code, folded under the card.

For each card:
1. Keep the grouping and the problems listed (they come from the TikTok deck). If a listed problem is not in the
   TikTok deck, keep it only if it is on a classic list (`research/companies/tiktok/catalog/other_lists.json`) or in
   `sources/local/lc-in-decks.json`; otherwise replace it with a TikTok-deck problem of the same variant.
2. At the end of the card, one folded block per listed problem, in list order:

   **例题：** LC 78 子集

   一两句题意（含关键约束）。

   ```python
   <the main solution from that problem's whole-answer card
    vault/interviews/core/leetcode/tiktok/cards/*/tlc-<slug>-0-whole.md (comments and blank lines may go, logic unchanged);
    for a non-TikTok problem take the code from sources/local/lc-in-decks.json>
   ```

3. Verify every block runs on the problem's first example (scratch harness).

Gate: `uv run python research/companies/tiktok/tools/gate_cards.py <your files>` (0 problems),
`uv run python scripts/plain_style.py <your files>` ok, `uv run trellis --domain tiktok-lc validate` 0 errors.

Reply (≤ 8 lines): cards done, blocks added, problems replaced, anything left without code.
