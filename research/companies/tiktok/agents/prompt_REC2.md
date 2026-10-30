# Revise agent — TikTok decks: recursion first (group R2)

Repo `/Users/chiserver/sessions/trellis`, branch `main`. Never commit, never spawn agents, edit only the cards of your
leaves. Scratch in `/tmp/rec_R2/`. `git checkout uv.lock` whenever uv touches it.

Read the section "Recursion first" at the end of `research/companies/tiktok/CARDS.md` (and the rest of that file for
card shape and the gate). Chi (2026-10-30): explicit-stack rewrites made only to avoid Python's recursion limit are
over-engineering; he wants the intuitive recursive solution first and the stack version as an extra.

**Your leaves** (cards: `vault/interviews/core/leetcode/tiktok/cards/<band>/tlc-<slug>-0-whole.md` and
`vault/interviews/core/leetcode/tiktok-drill/cards/<band>/tlc-<slug>-*.md`, `<band>` = the part before the dot):
p1.tt-islands-follow-ups, p2.making-a-large-island, p3.decode-string, p3.restore-ip-addresses, p3.tt-deep-merge-nested-json, p3.word-search-ii, p4.balanced-binary-tree, p4.double-a-number-represented-as-a-linked-list, p4.maximum-depth-of-binary-tree, p4.partition-array-for-maximum-sum, p4.recover-binary-search-tree, p4.tt-all-simple-paths, p4.validate-binary-search-tree, p5.amount-of-time-for-binary-tree-to-be-infected, p5.most-frequent-subtree-sum, p5.tt-flatten-multilevel-list-skip-empty, b.binary-tree-cameras, b.codetop-supp-4, b.convert-binary-search-tree-to-sorted-doubly-linked-list, b.house-robber-iii, b.lowest-common-ancestor-of-deepest-leaves, b.minimum-distance-between-bst-nodes, b.number-of-good-leaf-nodes-pairs, b.reorder-list, b.walls-and-gates

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
