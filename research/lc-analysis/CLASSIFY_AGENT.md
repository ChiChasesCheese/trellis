# LeetCode classification agent: technique and pitfall tags for every solved problem

Repo `/Users/chiserver/sessions/trellis`. Never commit, never spawn agents. Scratch in `/tmp/lc_<task>/`. Outputs go to
`sources/local/lc/` (gitignored). **Resume rule:** skip any slug already present in your output file.

Chi wants to see, across his LeetCode decks, which **techniques** (思路 / 思维) and which **pitfalls** (易错点) he holds and
which he keeps getting wrong. Patterns (题型) already come from `vault/interviews/core/leetcode/knowledge-map/` and syntax
is parsed from code, so your job is the two dimensions only a reader can judge.

Input: `sources/local/lc/sections.jsonl`, one problem per line: `slug`, `title`, `idea` (一句话), `signal` (识别),
`pitfalls` (易错点). Read only these; open a full body in `vault/interviews/core/leetcode/problems/<slug>.md` only when a
line is ambiguous.

## Task T: the taxonomy (`sources/local/lc/taxonomy.json`)

Read every line's `idea` and `signal` (skim; script it into chunks) and build two controlled vocabularies:

- **techniques**: 60–90 entries. Each is one reusable move a candidate must recognise and execute, at the grain an
  interviewer probes: 「可变长滑动窗口（左端跳到重复位置之后）」, 「单调栈找下一个更大元素」, 「前缀和 + 哈希计数」, 「二分答案（判定函数单调）」,
  「多源 BFS」, 「记忆化 DFS 转自底向上 DP」. Not a whole pattern (too coarse: 「滑动窗口」) and not one problem's trick (too
  fine). Each entry: `id` (kebab-case English), `name` (Chinese, English term in parentheses), `pattern` (one of the
  knowledge-map file stems: 01-hashing … 22-math-bit), `signal` (one line: when to reach for it).
- **pitfalls**: 15–25 categories of mistake, defined so two readers would put the same bullet in the same box:
  off-by-one in loop bounds, empty / single-element input, integer overflow or precision, duplicates handling,
  visited marking timing (on push vs on pop), recursion base case / depth limit, mutating while iterating, shallow copy
  of path in backtracking, wrong invariant on window shrink, comparator / heap order (max vs min), 0- vs 1-indexing in
  DP tables, unhandled disconnected graph, cycle in linked list pointers, Python-specific traps (mutable default,
  `heapq` is min-only, `sorted` vs `.sort()`), complexity trap (accidentally quadratic). Each: `id`, `name`, `definition`.

Write `{"techniques": [...], "pitfalls": [...]}` and stop.

## Task C: classify (`sources/local/lc/tags_<part>.jsonl`)

For each slug in your range (by line number in sections.jsonl), one line:
`{"slug": ..., "techniques": [1–3 technique ids, main first], "pitfalls": [pitfall ids, one per 易错点 bullet that fits,
deduplicated], "insight": "<the one thinking step that unlocks it, ≤ 30 Chinese characters>"}`.
Use only ids from taxonomy.json. If a bullet fits no category, leave it out rather than stretching one. If a problem
truly needs a technique the taxonomy lacks, use the closest and add `"gap": "<what is missing>"`.

## Gate

`python3 -c` check: every slug in range present once, every id exists in taxonomy.json, no empty `techniques`.
Reply in ≤ 5 lines: count done, the 5 most used techniques and pitfalls, any taxonomy gaps.
