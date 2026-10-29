# Task — TikTok LeetCode decks: rewrite 2-D DP cards to the full table (DB)

Repo `/Users/chiserver/sessions/trellis`, branch `main`. Never switch branches, never commit, never spawn agents.
Scratch work in `/tmp/dp_DB/`. `git checkout uv.lock` whenever uv touches it. Other agents write cards in the
same folders at the same time: touch only the files named below, never a wildcard over a folder.

## The rule (from Chi, the learner)

Chi finds rolling-array DP hard to follow. Read the section "2-D DP: full table, no rolling" at the end of
`research/companies/tiktok/CARDS.md`, and the rest of that file for card shape and the gate.

## Your files

Problem leaves (tier B): b.combination-sum-ii b.first-day-where-you-have-been-in-all-the-rooms b.frog-jump b.jump-game-ii b.last-stone-weight-ii b.longest-mountain-in-array b.longest-repeating-substring b.longest-string-chain b.matchsticks-to-square b.maximum-length-of-repeated-subarray b.min-cost-climbing-stairs b.minimum-cost-good-caption b.minimum-moves-to-spread-stones-over-grid b.minimum-operations-to-make-character-frequencies-equal b.partition-array-for-maximum-sum b.partition-equal-subset-sum b.super-egg-drop b.triangle b.xun-bao

Also:
- The pattern cards `vault/interviews/core/leetcode/tiktok/cards/patterns/tlc-patterns-dp-grid-string-*.md` and
  `tlc-patterns-dp-knapsack-*.md`: their **template** cards must show the full 2-D table; move any rolled template out
  (one pointer line to 「Python 工具箱「DP 降维」」).
- **New leaf `python.dp-space-compression`** (title「DP 降维：滚动数组与空间压缩」, already in `skeleton/tiktok-lc.yaml`):
  write 7 cards in `vault/interviews/core/leetcode/tiktok/cards/python/`, ids `tlc-python-dp-space-compression-<n>-<slug>`,
  `node: python.dp-space-compression`, `type: qa`, `step: <n>`, shaped like the other `tlc-python-*` cards. Teach from
  zero, assuming Chi has only seen full 2-D tables; each card has a small runnable example with real output, the 2-D
  version first and the compressed one next to it:
  1. When a table can shrink: draw which cells `dp[i][j]` reads; only the previous row (and the current row) → keep rows.
  2. Two rows (`prev` / `cur`), on Unique Paths or Minimum Path Sum.
  3. One row in place: reading up (old value) and left (new value) — why forward order works for grids.
  4. 0-1 knapsack must go backwards, complete knapsack forwards (LC 416 vs LC 518), with the wrong output each way.
  5. Upper-left (diagonal) dependency — LCS / edit distance need an extra variable for the old diagonal; the bug without it.
  6. When not to compress: you must output the path / the plan, or an interval DP by length; in an interview write the
     2-D table first, then offer the compression.
  7. Problems in this deck that take each form (LC numbers and names), grouped by card 2–5.

For each problem leaf `<tier>.<slug>`, its cards are `vault/interviews/core/leetcode/tiktok/cards/<tier>/tlc-<slug>-0-whole.md`
(whole card) and `vault/interviews/core/leetcode/tiktok-drill/cards/<tier>/tlc-<slug>-{1..5}-*.md` (split cards).

1. Read the whole card. If the problem's DP state is 1-D, or the solution is not DP, or it already uses a full 2-D table
   (or top-down `@cache` over two indices), leave all its cards alone.
2. Otherwise rewrite the main solution as a bottom-up full 2-D table in the whole card and the `-2-code` card: clear
   state definition (`dp[i][j]` = …), base row / column, transition, answer cell. Re-run the code in `/tmp/dp_DB/`
   on the statement's examples and against a brute force on ≥ 300 random small inputs; the **运行** outputs on the cards
   must be the real ones. Update **复杂度** (space becomes O(mn)), **思路 / 推导 / 写法要点**, and any **易错点** or `-3-why`
   counterexample that was about the rolling array (e.g. iteration direction): replace it with a pitfall of the 2-D
   version (an off-by-one in the base row, a wrong transition), with a concrete wrong output.
3. Remove rolled code from the `-4-followup` card and 追问; leave one line:「空间可以压到 O(n)：见 Python 工具箱「DP 降维」」.
4. Whole card and split cards must agree (same code, same complexity, same counterexample).
5. Gate on every file you changed: `uv run python research/companies/tiktok/tools/gate_cards.py <files>`,
   `uv run python scripts/plain_style.py <files>`, then `uv run trellis --domain tiktok-lc validate` and
   `uv run trellis --domain tiktok-lc-drill validate` (0 errors).

## Reply (≤ 12 lines)

Problems rewritten, problems checked and left alone (one word why each), gate results, and any claim you are unsure of.
