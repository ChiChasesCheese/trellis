# Card agent — TikTok deck tier C: whole-answer cards only (groups C1 / C2 / C3)

Repo `/Users/chiserver/sessions/trellis`, branch `main`. Never switch branches, never commit, never spawn agents, never
edit files you do not own. Scratch work goes in `/tmp/tlc_<group>/`, never in the repo.

Chi (2026-10-31) wants every problem the US TikTok / ByteDance LeetCode company lists carry to be in the deck. Tier C
holds the ones seen only more than six months ago with low frequency. They get **one whole-answer card each and no split
cards**.

**How to write the card:** follow `research/companies/tiktok/agents/prompt_Y1.md` sections 1, 2, 3a (including its
**Code rules**), 5, "Main problem first" and "2-D DP: full table", plus `research/companies/tiktok/CARDS.md` (recursion
first). Ignore that file's leaf list, its section 3b (no split cards here) and section 4. Leaf ids are `c.<slug>`, so
cards go to `vault/interviews/core/leetcode/tiktok/cards/c/tlc-<slug>-0-whole.md` with `node: c.<slug>`. The header
line is `**LC n 中文名**｜<Easy|Medium|Hard>` (the frequency facts are stamped later by a script). Statement:
`sources/local/tiktok-lc/<slug>.txt` (copy constraints from it). Premium problems whose statement is in English only:
translate faithfully. JavaScript-only problems (e.g. Event Emitter, Flatten Deeply Nested Array): solve the same task in
Python with the closest Python data model and say so in one line on the front.

Also add, like the deck's P1/P2 cards: `**简单解法。**` right after **推导** (the most direct correct solution — brute
force or a simpler slower method — with a complete ```python block, its complexity and one sentence on where it stops
being enough; the main code then follows under 「最优解：」) and `**拓展优化。**` right after **复杂度** (1–2 bullets of
optimisations / extensions, code where more than a one-line change). If the simplest solution is already optimal,
the brute force is the 简单解法.

**Resume rule:** `ls vault/interviews/core/leetcode/tiktok/cards/c/`; skip leaves that already have their card.

Reply (≤ 8 lines): cards written, problems you translated from English or moved from JavaScript, anything unverified.

## Comments carry the explanation (Chi, 2026-10-31)

Put the reasoning **inside the code as short Chinese comments** (what each block does and why: the invariant, why this
pointer moves, why this boundary). Clear names and comments replace prose: do not repeat in a paragraph what the code
and its comments already say. **推导** stays a short paragraph; prose around each code block is at most one or two
sentences. Lowest reading cost wins.
## What 简单解法 is (Chi, 2026-10-31, replaces the earlier wording)

"不不不这种就不需要暴力解了！我的意思是不必要的 或者比较细节的优化 比如不 dfs 而是先建 trie 或者先 bfs 记录 valid 点那几个".
`**简单解法。**` exists only when the main solution carries an optimisation that is optional or detail-heavy (a trie built
first instead of plain DFS, a BFS pre-pass that records valid cells, pruning, an extra index structure, a constant-space
trick, a hand-made linked list where `OrderedDict` would do). The simple solution is the same core idea **without** that
refinement, still an acceptable interview answer. When the main solution is already the most direct correct one, write
**no** 简单解法 section and no 「最优解：」 lead — never fill it with an exhaustive brute force or a worse algorithm nobody
would write.
