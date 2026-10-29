# Task — TikTok LeetCode decks: rewrite 2-D DP cards to the full table (DA)

Repo `/Users/chiserver/sessions/trellis`, branch `main`. Never switch branches, never commit, never spawn agents.
Scratch work in `/tmp/dp_DA/`. `git checkout uv.lock` whenever uv touches it. Other agents write cards in the
same folders at the same time: touch only the files named below, never a wildcard over a folder.

## The rule (from Chi, the learner)

Chi finds rolling-array DP hard to follow. Read the section "2-D DP: full table, no rolling" at the end of
`research/companies/tiktok/CARDS.md`, and the rest of that file for card shape and the gate.

## Your files

Problem leaves (tier A): a.best-time-to-buy-and-sell-stock a.best-time-to-buy-and-sell-stock-ii a.best-time-to-buy-and-sell-stock-iv a.binary-tree-maximum-path-sum a.cheapest-flights-within-k-stops a.climbing-stairs a.coin-change a.coin-change-ii a.combination-sum a.distinct-subsequences a.edit-distance a.generate-parentheses a.house-robber a.interleaving-string a.jump-game a.longest-common-subsequence a.longest-increasing-path-in-a-matrix a.longest-increasing-subsequence a.longest-palindromic-substring a.longest-valid-parentheses a.maximal-square a.maximum-subarray a.maximum-subarray-sum-with-one-deletion a.minimum-path-sum a.numbers-at-most-n-given-digit-set a.palindrome-partitioning a.partition-to-k-equal-sum-subsets a.regular-expression-matching a.stickers-to-spell-word a.target-sum a.text-justification a.trapping-rain-water a.tt-valid-parenthesis-string-print-all a.unique-paths a.valid-parenthesis-string a.wildcard-matching a.word-break a.word-break-ii

For each problem leaf `<tier>.<slug>`, its cards are `vault/interviews/core/leetcode/tiktok/cards/<tier>/tlc-<slug>-0-whole.md`
(whole card) and `vault/interviews/core/leetcode/tiktok-drill/cards/<tier>/tlc-<slug>-{1..5}-*.md` (split cards).

1. Read the whole card. If the problem's DP state is 1-D, or the solution is not DP, or it already uses a full 2-D table
   (or top-down `@cache` over two indices), leave all its cards alone.
2. Otherwise rewrite the main solution as a bottom-up full 2-D table in the whole card and the `-2-code` card: clear
   state definition (`dp[i][j]` = …), base row / column, transition, answer cell. Re-run the code in `/tmp/dp_DA/`
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
