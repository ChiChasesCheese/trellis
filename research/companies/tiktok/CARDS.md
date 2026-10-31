# Card agent — TikTok / ByteDance top-frequency LeetCode deck (`tiktok-lc`), group {GROUP}

Repo `/Users/chiserver/sessions/trellis`, branch `main`. Never switch branches, never commit, never spawn agents, never
edit files you do not own. Scratch work goes in `/tmp/tlc_{GROUP}/`, never in the repo.

**You own these leaves** (write their cards, nothing else): {LEAVES}

Cards go to `vault/interviews/core/leetcode/tiktok/cards/<branch>/` where `<branch>` is the part of the leaf id before
the dot (`a`, `b`, `python`, `patterns`). File name = card id + `.md`.

## 0. Resume rule

`uv run trellis --domain tiktok-lc stats` and `ls` your folders; skip leaves that already have their cards.
`git checkout uv.lock` whenever uv touches it.

## 1. Read first

- The pilot — copy its shape exactly: `vault/interviews/core/leetcode/tiktok/cards/a/tlc-longest-substring-without-repeating-characters-*.md` (4 files).
- `skeleton/tiktok-lc.yaml` (leaf titles), `research/companies/tiktok/index.json` (difficulty, frequency, tags).
- For each problem, its statement: `sources/local/tiktok-lc/<slug>.txt`. **Copy constraints from this file, never from
  memory** (a past deck shipped wrong ranges written from memory).
- `proposals/WRITING_RULES.md` rules 1, 3, 5, 6, 11, 12.

## 2. Who reads these cards

Chi, a senior engineer preparing for TikTok / ByteDance coding rounds, wants to finish this deck and find LeetCode
interviews easy. Two things beyond a plain solution: **deep intuition and pattern recognition** (which signals in the
statement point to which technique, and how to get from brute force to the optimum), and **advanced, idiomatic Python**
(the standard library used well, with the reason each idiom is better). Chinese prose, English terms in parentheses,
code identifiers in backticks, code comments in Chinese.

## 3a. Problem leaves: first, ONE whole-answer card (the source of truth)

Chi (2026-10-24): the deck splits in two. Deck **整题答案** has exactly one card per problem — a thorough best-practice
answer he goes through first. Deck **拆分背诵** holds the split cards of 3b, for warm-up before interviews. You write
both kinds in the same folder; the orchestrator files the split ones into their deck.

The whole card: id `tlc-<slug>-0-whole`, file `tlc-<slug>-0-whole.md`, **no `step:` line**. Copy the pilot
`tlc-longest-substring-without-repeating-characters-0-whole.md` exactly in shape:
- Front: header line, the full statement in Chinese with all constraints and 1–2 examples, then「给出完整的最优解答：识别、推导、
  代码、复杂度、易错点、追问。」
- Back: **一句话** (the whole idea in one sentence) · **识别** (the signals) · **推导** (brute force → waste → insight →
  optimum, one paragraph) · the full solution in one ```python block · **运行** (real outputs) · **复杂度** · **易错点**
  (2–3 bullets, with a concrete wrong output where possible) · **追问** (2–3 bullets, one line each) · **同模式**.
- It may be long (a word-count warning on `-0-whole` cards is expected and fine); it must still be self-contained.
- The whole card and the split cards must agree (same code, same complexity, same counterexample).

## 3b. Problem leaves: then the split cards — 4 each (5 for Hard)

| step | file suffix | front | back |
|---|---|---|---|
| 1 | `-1-signal` | header line `**LC n 中文名**｜难度 · TikTok 高频` (or 字节 / TikTok·字节), the statement restated faithfully in Chinese with **all constraints** from the statement file and one example; then「题面里哪些信号指向哪个模式？从暴力解怎样一步步推到最优解？」 | **信号 → 模式** (2–4 bullets: each signal and what it implies, incl. what `n` allows), **推导链** (numbered: brute force and its cost → the waste → the key insight → the optimum), **同模式的题** (2–4 LC numbers + names) |
| 2 | `-2-code` | header `｜写出 Python 实现` + a one-paragraph restatement with constraints | **思路** (2–3 sentences), the full solution in a ```python block, **运行** (the real outputs on the statement's examples and 1–2 edge cases), **复杂度** (time and space with the reason), **写法要点** (the idioms used and why) |
| 3 | `-3-why` | header `｜正确性` + a question about the invariant or the step people get wrong | the invariant, why the solution keeps it, and a **concrete counterexample** that breaks the tempting wrong version (state the wrong output and the right one) |
| 4 | `-4-followup` | header `｜追问` + 2–3 follow-ups an interviewer actually asks (return the path, stream input, memory limit, k variants, scale) | how each one changes the solution, with short code where it helps; one **Python 提醒** line on a library pitfall |
| 5 (Hard only) | `-5-alt` | header `｜另一种解法` | a second approach (or the brute force that is acceptable for small n), and when to prefer which |

Card id: `tlc-<slug>-<suffix>`; `node: <leaf id>`; `type: qa`; `step: <n>`. Frontmatter exactly like the pilot.

**Code rules** (checked by the gate):
- Full, runnable solution in a plain function (or a class for design problems) with **type hints on every parameter and
  the return**; Python 3.12+ built-in generics (`list[int]`, `dict[str, int]`, `X | None`). Use `ListNode` / `TreeNode`
  / `Node` names as LeetCode does (the gate defines them).
- Idiomatic and advanced where it helps: `collections` (`Counter`, `defaultdict`, `deque`), `heapq`, `bisect`,
  `itertools` (`accumulate`, `pairwise`, `groupby`), `functools.cache`, `enumerate`/`zip`, unpacking, walrus when it reads
  better. Never a one-liner that hides the technique the interview tests (e.g. `bin(int(a,2)+int(b,2))` for add-binary).
- **Run every solution** in `/tmp/tlc_{GROUP}/`: on the statement's examples, on edge cases, and **against a brute force
  on ≥ 300 random small inputs** whenever a brute force is writable. Test the upper constraint once for recursion depth
  (`RecursionError` at depth > 1000 means: rewrite iteratively or justify). The outputs on the card are the real ones.
- Never write the verification process on a card (no "对拍", "随机测试"); the card states facts and outputs.

## 4. Python and pattern leaves (only if you own them): 6–9 cards each

- `python.*`: each card one idiom or library point — what it does, the complexity, a 3–8 line example with real output,
  when to use it, the pitfall. Tie each to a problem type ("Top-K 用 `heapq.nlargest`…").
- `patterns.*`: cards in this order: **signals** (what in a statement triggers the pattern, and the near-miss signals
  that look similar but need something else), **template** (a reusable Python template with type hints), **why it is
  correct** (the monotonicity / invariant), **variants** (the 3–5 problem shapes and how the template bends), **pitfalls**,
  **problems** (8–15 LC problems from this deck that use it, by number and name, grouped by variant).

## 5. Gate (before replying)

1. `uv run python research/companies/tiktok/tools/gate_cards.py <your files>` — 0 problems.
2. `uv run python scripts/plain_style.py <your files>` — ok.
3. `uv run trellis --domain tiktok-lc validate` — 0 errors; no `not_self_contained` / `leans_on_source` on your cards.
   A long-answer warning (> 250 words) is acceptable only on `-0-whole` and `-2-code` cards; split any other card.
4. `git checkout uv.lock` if changed.

## 6. Reply (≤ 12 lines)

Cards per leaf range, gate results, how many solutions were checked against a brute force, any statement file that
looked truncated or wrong, and up to 6 claims you are least sure of.

## China-side problems (剑指 Offer, 补充题)

Some leaves come from China-side ByteDance interviews. Use the statement file. Four `补充题` (`codetop-supp-1`, `-2`,
`-9`, `-23`) have **no statement file**: restate the classic problem precisely from knowledge (排序奇升偶降链表, 圆环回原点
问题, 36 进制加法, 检测循环依赖), choose sensible constraints, and list those leaves in your reply. Header line for those:
`**补充题 n 中文名**｜难度 · 字节高频`; for 剑指 Offer: `**剑指 Offer n 中文名**｜难度 · 字节高频`.

## TikTok variants (`tt-*` leaves) and newly reported LeetCode problems

`tt-*` leaves are TikTok-specific problems reconstructed from interview reports; their statement file ends with a note
on which parts were inferred — use it to choose sensible constraints, but **never put provenance or "reconstructed"
on a card**: the card states the problem as the problem. Header line `**中文题名**｜难度 · TikTok 高频` (pick the
difficulty yourself). Design-style variants (LRU with TTL, KV store with snapshot, scheduler …) get a class with type
hints; verify them with your own unit tests and a randomized comparison against a naive reference implementation
(≥ 300 random operation sequences). Their follow-up card covers the follow-ups listed in the statement file.

## Where split cards go (updated 2026-10-24)

Write each problem's `-0-whole` card into `vault/interviews/core/leetcode/tiktok/cards/<branch>/` and its split cards
(`-1-signal` … `-5-alt`) **directly into `vault/interviews/core/leetcode/tiktok-drill/cards/<branch>/`** (the drill
deck). Run the gate's `validate` for both domains: `trellis --domain tiktok-lc validate` and
`trellis --domain tiktok-lc-drill validate`.

- Never move, rename or delete files that are not your own leaves' cards: match your exact slugs, never a wildcard over a whole folder (other agents write in the same folders at the same time).

## Main problem first (2026-10-28)

When a statement has a main task and a follow-up (追问), the whole card and the `-2-code` card solve the **main task**;
the follow-up's technique goes into **追问** / the `-4-followup` card (idea first, code after). Never promote a
follow-up into the main requirement: a card that opens with a Fenwick tree for what is LC 528 plus a discussion
follow-up teaches the wrong priorities.

## 2-D DP: full table, no rolling (Chi, 2026-10-28)

For any DP whose natural state has two indices (grid, two strings, interval, knapsack item × capacity, including
0-1 / complete knapsack counting such as LC 416, 494, 518), the main solution on the whole card and the `-2-code` card
uses the **full 2-D table** (`dp = [[0] * (n + 1) for _ in range(m + 1)]`), never a rolling array, a single reused row
or a 1-D reduction. Space reduction appears only as one line in 追问 / the `-4-followup` card:「空间可以压到 O(n)：见
Python 工具箱「DP 降维」」, without code. The technique itself lives in leaf `python.dp-space-compression`. 1-D DP
(state `dp[i]`) is unaffected.

## Header stats (2026-10-29)

Keep writing the header as `**LC n 中文名**｜<难度> · TikTok 高频`; `tools/stamp_headers.py` then replaces everything after
the difficulty with the data (company-tag frequency, sightings in the past year, CodeTop count, most recent date).

## Recursion first (Chi, 2026-10-30)

For any problem whose natural solution is a recursive DFS (trees, graphs, grids, nested structures, backtracking), the
whole card and the `-2-code` card show the **most intuitive recursive version** as the main solution — never an
explicit-stack rewrite made only to dodge Python's recursion limit. Then:
- **易错点** gets one line: worst-case depth (for example a chain of `n` nodes) and that CPython's default limit is about
  1000, so a depth above that raises `RecursionError` unless `sys.setrecursionlimit` is raised or the code is iterative.
- The explicit-stack version goes to **追问** (whole card) and the `-4-followup` card (or `-5-alt`), with its code.
Solutions where a stack *is* the natural algorithm (expression evaluation, decode string, monotonic stack, an
explicitly iterative traversal the problem asks for) are unaffected.

## Pattern-card examples (Chi, 2026-10-31)

An example on a pattern card is either tier A (bands p1–p4) or a problem that is also on another list (Chi's Amazon or
topic decks, Blind 75, NeetCode 150, LeetCode Hot 100, Top Interview 150 — `catalog/other_lists.json`). Tier-B problems
that are on no other list do not appear as examples.

## Comments carry the explanation (Chi, 2026-10-31)

"注意代码里面来点注释 尽量能注释和优秀代码能解释的就不要额外文字段落重复 尽量阅读成本降低." The reasoning lives inside
the code as short Chinese comments (each block's purpose, the invariant, why a boundary or pointer move is right). Prose
never restates what the code and its comments already say; around a code block it is one or two sentences at most.
