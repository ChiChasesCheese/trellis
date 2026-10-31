# Revise agent — TikTok whole-answer cards: add 简单解法 and 拓展优化 (groups SO1 / SO2)

Repo `/Users/chiserver/sessions/trellis`, branch `main`. Never commit, never spawn agents, edit only the whole cards of
your problems: `vault/interviews/core/leetcode/tiktok/cards/<band>/tlc-<slug>-0-whole.md` (band = the part of the leaf
id before the dot). Scratch in `/tmp/so_<group>/`. `git checkout uv.lock` whenever uv touches it. Card rules:
`research/companies/tiktok/CARDS.md` (read it first; recursion first, 2-D DP as a full table, main problem first).

Chi (2026-10-31): these problems appeared on the US TikTok / ByteDance LeetCode lists in the last six months, so they are
now P1/P2 and must be remembered firmly. He wants to learn **both the simple solution and the optimisations**.

**Resume rule:** skip a card that already has a `**简单解法。**` label.

For each card add two labelled sections, keeping everything else unchanged (the existing main solution stays the main
solution):

1. `**简单解法。**` — placed right after **推导** and before the main ```python block. The most direct correct solution
   a candidate can write in five minutes under pressure: the brute force when it is still correct, or a simpler
   slower method (e.g. sort instead of heap, BFS by levels instead of Dijkstra, OrderedDict instead of a hand-made
   linked list). One or two sentences on the idea, a complete ```python block (type hints, same function signature as
   the main one), its time / space, and one sentence on where it stops being good enough (which constraint it fails,
   or that it is acceptable as an opening answer). If the main solution is already the simplest correct one, give the
   brute force instead. The main code then follows under a one-line lead 「最优解：」.
2. `**拓展优化。**` — placed right after **复杂度**. One to three optimisations or extensions an interviewer pushes
   toward (faster method, early exit, streaming input, returning the path, a second classic approach), each as a bullet
   with one sentence of idea and, where it is more than a one-line change, a short complete ```python block. Move a
   追问 bullet here when it is really an optimisation (don't repeat it in 追问). Space compression of a 2-D DP is never
   written out — one line pointing to Python 工具箱「DP 降维」 is enough.

Every new code block is run in your scratch folder on the card's examples and against the main solution on ≥ 300
random small inputs (when inputs are generable). Write the real outputs; never mention the testing on the card.
Chinese prose, English terms in parentheses, code comments in Chinese.

Gate: `uv run python research/companies/tiktok/tools/gate_cards.py <your files>` (0 problems),
`uv run python scripts/plain_style.py <your files>` ok, `uv run trellis --domain tiktok-lc validate` 0 errors.

Reply (≤ 8 lines): cards done, cards where the simple solution is the brute force, anything you could not verify.

## Comments carry the explanation (Chi, 2026-10-31)

Put the reasoning **inside the code as short Chinese comments** (what each block does and why: the invariant, why this
pointer moves, why this boundary). Clear names and comments replace prose: do not repeat in a paragraph what the code
and its comments already say. Prose around a code block is at most one or two sentences (the idea in one line, the
complexity, where it stops being enough). Lowest reading cost wins. When you touch a card, also trim existing prose
that only restates the code, moving any non-obvious point into a comment.
