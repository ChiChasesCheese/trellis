# Revise agent — TikTok decks: recursion first (group R3)

Repo `/Users/chiserver/sessions/trellis`, branch `main`. Never commit, never spawn agents, edit only the cards of your
leaves. Scratch in `/tmp/rec_R3/`. `git checkout uv.lock` whenever uv touches it.

Read the section "Recursion first" at the end of `research/companies/tiktok/CARDS.md` (and the rest of that file for
card shape and the gate). Chi (2026-10-30): explicit-stack rewrites made only to avoid Python's recursion limit are
over-engineering; he wants the intuitive recursive solution first and the stack version as an extra.

**Your leaves** (cards: `vault/interviews/core/leetcode/tiktok/cards/<band>/tlc-<slug>-0-whole.md` and
`vault/interviews/core/leetcode/tiktok-drill/cards/<band>/tlc-<slug>-*.md`, `<band>` = the part before the dot):
p2.basic-calculator, p2.tt-basic-calculator-ladder, p3.generate-parentheses, p3.possible-bipartition, p3.subtree-of-another-tree, p3.tt-max-path-sum-with-path, p4.delete-node-in-a-bst, p4.find-distance-in-a-binary-tree, p4.merge-two-sorted-lists, p4.number-of-atoms, p4.sort-an-array, p4.tt-hyper-operation, p4.tt-valid-parenthesis-string-print-all, p5.kth-smallest-element-in-a-bst, p5.populating-next-right-pointers-in-each-node, p5.tt-inorder-string-iterator, b.binary-tree-longest-consecutive-sequence, b.combination-sum-ii, b.find-largest-value-in-each-tree-row, b.invert-binary-tree, b.matchsticks-to-square, b.minimum-depth-of-binary-tree, b.path-sum-ii, b.scramble-string, b.vertical-order-traversal-of-a-binary-tree

For each leaf: read the whole card. If its main solution is an iterative rewrite of a naturally recursive DFS, rewrite
the main solution (whole card + `-2-code`) as the clearest recursive version, update 思路 / 推导 / 写法要点 / 复杂度 and
易错点 (one line about depth and the recursion limit), move the stack version into 追问 and `-4-followup` (or keep it as
`-5-alt` if that card already holds an alternative). Keep whole and split cards consistent; re-run the code (examples
and ≥ 300 random small inputs against the old solution as reference); the 运行 outputs must be real. If the main
solution is already recursive or the stack is the natural algorithm, leave the leaf alone.

Gate: `uv run python research/companies/tiktok/tools/gate_cards.py <changed files>` (0 problems; raise the recursion
limit in your own tests if needed), `uv run python scripts/plain_style.py <changed files>` ok, `uv run trellis --domain
tiktok-lc validate` and `--domain tiktok-lc-drill validate` 0 errors.

Reply (≤ 8 lines): leaves rewritten, leaves left alone (one word why), gate results.
