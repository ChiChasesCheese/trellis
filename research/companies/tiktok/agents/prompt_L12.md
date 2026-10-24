# Card agent — TikTok / ByteDance top-frequency LeetCode deck (`tiktok-lc`), group L12

Repo `/Users/chiserver/sessions/trellis`, branch `main`. Never switch branches, never commit, never spawn agents, never
edit files you do not own. Scratch work goes in `/tmp/tlc_L12/`, never in the repo.

**You own these leaves** (write their cards, nothing else): `b.missing-ranges`, `b.summary-ranges`, `b.product-of-array-except-self`, `b.number-of-connected-components-in-an-undirected-graph`, `b.house-robber-iii`, `b.nested-list-weight-sum`, `b.mini-parser`, `b.most-frequent-subtree-sum`, `b.permutation-in-string`, `b.beautiful-arrangement-ii`, `b.number-of-distinct-islands-ii`, `b.min-cost-climbing-stairs`, `b.ip-to-cidr`, `b.swim-in-rising-water`, `b.minimum-add-to-make-parentheses-valid`, `b.binary-tree-cameras`, `b.time-based-key-value-store`, `b.vertical-order-traversal-of-a-binary-tree`, `b.longest-string-chain`, `b.maximum-length-of-a-concatenated-string-with-unique-characters`, `b.minimum-swaps-to-make-strings-equal`, `b.number-of-days-between-two-dates`, `b.kth-smallest-subarray-sum`, `b.parallel-courses-iii`, `b.successful-pairs-of-spells-and-potions`, `b.amount-of-time-for-binary-tree-to-be-infected`, `b.count-of-interesting-subarrays`, `b.maximize-amount-after-two-days-of-conversions`

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
- **Run every solution** in `/tmp/tlc_L12/`: on the statement's examples, on edge cases, and **against a brute force
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
