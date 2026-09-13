# ps11 · Factory Cost — cumulative build cost + adjacency distance penalty + bounded skip (DP)

**Sources（来源）：** PracHub 词条《Minimize total factory cost with distance penalties》
(Stripe · Software Engineer · Coding & Algorithms · Medium · Technical/Phone Screen ·
last updated 2026-03-29) — `catalog/discovery/2026-09/C_batchA.md` `## C4` 记录的一句话
Quick Overview："modeling cumulative build costs with adjacency distance penalties and handling
variants such as skipping a factory"；本轮（2026-09-03）重新用 WebFetch 抓取该 URL 正文，返回
内容与 C_batchA.md 一致——仍然只有这句 Quick Overview，规则、输入输出格式、函数签名、样例
**均未拿到**（页面需要登录/未完全加载）。旁证：interviewdb.io 有裸标题「Factory Cost」的独立
词条（Coding/Phone，约 2026-08 更新）；1point3acres 有标题「Factory Cost Optimizer」（全站
WebFetch 403，正文未获取）。三个标题**不完全一致**，是否为同一道题**未证实**。

**Confidence（置信度）：低** — 仅"建厂累计成本 + 相邻惩罚 + 可跳过一个（或多个）工厂的 DP"这个
主题方向有依据，具体的成本公式、距离惩罚公式、"跳过"约束、输入输出格式、part 划分**全部是本
仓库自拟**，不是任何来源的原文。

> ⚠️ **重建题（非真题）**：本题面是根据 PracHub 上《Minimize total factory cost with distance
> penalties》的一句话概述——"累计建厂成本 + 相邻工厂距离惩罚 + 可跳过一个/多个工厂的动态规划"
> ——**自拟**的训练题。
> 真实题面从未公开——规则、输入格式、输出格式、part 划分**全部是本仓库编的**。
> 练它是为了覆盖 **A01（前缀和 + argmin 带 tie-break）、S06（整数分金额、显式舍入规则）、
> S13（闭区间/off-by-one）、S08（确定性排序与 tie-break）**，**不要把这里的输出格式当成真题
> 格式**去背。

## Context
Stripe's Global Payments Infrastructure team is planning new settlement-hub data centers
("factories") along a fixed payment corridor (candidate sites are already surveyed and given in
corridor order, west to east). Building a hub costs money. Building two hubs too close together
also costs money: nearby hubs duplicate peering contracts and redundant capacity, so a
**proximity penalty** table charges extra based on the distance between two *consecutively
built* hubs. Deferring (not building) a candidate site avoids its build cost but can also remove
— or worsen — the proximity penalty of its former neighbors, since they become adjacent to each
other instead. The team wants the cheapest overall build plan, first assuming everything gets
built, then allowing an increasing budget of deferred sites.

Positions are given in a straight line (mile markers), strictly increasing in input order — the
corridor order and the position order are the same thing.

## Input (stdin)
```
PART n
FACTORIES
<factory row>
<factory row>
...
PENALTIES
<penalty band row>
<penalty band row>
...
SKIP                (Part 4 only)
<k>                  (Part 4 only)
```
* `PART n` — `n` in {1,2,3,4}. The `FACTORIES` and `PENALTIES` literal marker lines are
  required and case-sensitive. The `SKIP` section (marker line + one integer line) is present
  **only** for Part 4; Parts 1–3 stop after the `PENALTIES` section. Blank lines are ignored;
  optional spaces around commas are tolerated.
* **Factory row**: `factory_id,position,build_cost`
  - `factory_id`: non-empty token, no commas, unique.
  - `position`: non-negative integer, mile marker on the corridor. Rows are given in strictly
    increasing `position` order (the input order **is** the corridor order) — this is a
    property of well-formed input, not something a solution needs to re-sort.
  - `build_cost`: a plain decimal string with **0–2 decimal digits**, no currency symbol, no
    thousands separator (`"5"`, `"5.0"`, `"5.00"`, `"12.50"` all valid; `"12.500"` is a format
    error). Parsed to integer **cents** — money is never represented as a float anywhere in the
    solution; there is nothing to round because the input never carries more precision than the
    cent, and a value with a third decimal digit is rejected rather than rounded.
  - 0 ≤ number of factory rows ≤ 100 (this is a phone-screen DP problem, not a 10^5-row OA —
    keep the whole table in memory and don't over-engineer the data structures; Part 4's DP is
    `O(n^2 * k)` and 100 keeps that comfortably fast even in pure Python).
* **Penalty band row**: `min_dist,max_dist,penalty`
  - `min_dist`, `max_dist`: non-negative integers; `max_dist` may be the **literal token `inf`**
    (lowercase, exact) meaning open-ended. The interval is **closed on both ends**:
    `[min_dist, max_dist]` — a distance exactly equal to either boundary is inside that band.
  - `penalty`: same decimal-string-to-cents rule as `build_cost`.
  - Bands **may appear in any order** in the input (sort by `min_dist` before using them — do
    not assume the file is sorted; this is the same discipline as ps02's rate tiers).
  - Bands are not guaranteed to cover every possible distance — a distance that falls in a gap
    between bands has **no matching penalty** and each part below defines exactly what that
    means for that part (it is a defined, tested condition, not a crash).
  - 0 ≤ number of penalty band rows ≤ 20.
* **`SKIP` section (Part 4 only)**: the marker line `SKIP` followed by one line holding a single
  non-negative integer `k`, the maximum number of factories that may be left unbuilt.
  `0 ≤ k ≤` (number of factories, possibly 0 if there are no factories).

## Output
Exactly what each part specifies below (1–2 lines), always terminated the same way the other
problems in this repo are: `"\n".join(lines) + "\n"` for a non-empty output, empty string for no
output at all.

## Rules

### Part 1 — cumulative build cost
Every candidate factory is built. `total = sum(build_cost for all factories)`.
Output: `TOTAL $x.xx`. Zero factories → `TOTAL $0.00`.

### Part 2 — add adjacency distance penalties
Every candidate factory is still built, in corridor order. For every pair of **consecutively
built** factories `(i, i+1)` (0-indexed by input order), compute
`distance = position[i+1] - position[i]` and look up the one penalty band whose closed interval
contains it. `total = sum(build_cost) + sum(matched penalty over every adjacent pair)`.

If **any** adjacent pair's distance falls in a gap (no band contains it), the computation is
undefined and the output is a single error line instead of a total:
`ERROR no penalty band for distance=<distance>` (the **first** such gap in corridor order, i.e.
smallest `i`, if more than one pair is affected — tie-break: lowest index first).

Zero or one factory → no adjacent pairs at all → `TOTAL` is just `sum(build_cost)` (never an
error, since there is nothing to look up).

### Part 3 — skip at most one factory (prefix-sum argmin)
Same model as Part 2, plus one more option: **leave at most one** factory unbuilt. Skipping
factory `j` (0-indexed):
* removes its `build_cost`,
* removes the (up to two) adjacent-pair penalties that touched it — `(j-1, j)` and `(j, j+1)`,
  whichever exist,
* and, **only if `j` has a built factory on both sides** (`0 < j < n-1`), adds one new "bridge"
  penalty for the pair `(j-1, j+1)` using the same band lookup on
  `position[j+1] - position[j-1]`.

Skipping is only ever considered among configurations that still leave **at least one** factory
built — with 0 or 1 factories present, "skip nothing" is the only candidate (see below).

A configuration (either "skip nothing" or "skip factory `j`") is **valid** only if every
adjacency penalty it actually needs (the untouched original pairs, plus the bridge pair when
applicable) matches a band. Precompute the `n-1` original pair penalties once (`None` where no
band matches) and use **prefix counts / prefix sums** over that array to evaluate every
candidate `j` in O(1) after that (this is the intended technique — see `A01` in
`skills_matrix.md` — not a fresh O(n) rescan per candidate `j`).

Pick the valid configuration with the lowest `total`. **Tie-break, in this exact order:**
1. "skip nothing" beats any "skip `j`" at equal cost;
2. among tied "skip `j`" options, the **smallest `j`** wins.

If **no** configuration is valid (neither "skip nothing" nor any single "skip `j`" clears every
band lookup it needs), output the single line `ERROR no valid configuration`.

Output (2 lines, unless the error case above applies):
```
TOTAL $x.xx
SKIPPED <factory_id>
```
`SKIPPED NONE` when the winning configuration is "skip nothing".

### Part 4 — skip up to k factories (DP with reconstruction)
Generalize Part 3: choose a subset of **at most `k`** factories to leave unbuilt (out of all
factories present) so as to minimize `sum(build_cost of built factories) + sum(adjacency
penalty between every pair of consecutively-built factories, in corridor order)`, where two
built factories are "consecutively built" if every factory between them (by original corridor
order) was left unbuilt.

At least one factory must remain built whenever there is at least one factory at all (you may
assume `k < n` in that case; `k` is not offered as "skip everything").

Use dynamic programming over `(last built index i, factories skipped so far s)`:
`dp[i][s]` = minimum cost of a plan whose last built factory is `i` and which has skipped `s`
factories among `0..i-1`. A transition from a previous built factory `j < i` to `i` skips
`i - j - 1` factories (those strictly between them) and adds `build_cost[i]` plus the band
penalty for `position[i] - position[j]`; the base case (`i` is the very first built factory)
skips `i` factories (those before it) and adds only `build_cost[i]`. A transition whose skip
count would exceed `k`, or whose required band lookup has no match, is invalid and excluded.

**Tie-break (again, exact order — this is what makes the reconstructed plan deterministic):**
1. lower `dp[i][s]` wins outright;
2. at equal `dp[i][s]`, prefer the transition that skips **fewer** factories in that one step
   (i.e. the **larger** `j`, the closest earlier built candidate) — "prefer to keep building
   over deferring" whenever it's free to do so;
3. among the final terminal states (`i`, `s`) that reach the global minimum total cost, prefer
   the one with the **fewest total factories skipped** (`s` plus however many trailing factories
   after `i` are left unbuilt);
4. if still tied, prefer the **largest** last-built index `i` (fewest trailing skips).

If no plan exists within the `k` budget (every reachable chain needs a band lookup that has no
match, or the required skip count would exceed `k`), output the single line
`ERROR no valid configuration within skip budget k=<k>`.

Output (2 lines, unless the error case above applies):
```
TOTAL $x.xx
SKIPPED <comma-joined factory_ids of every skipped factory, in corridor order>
```
`SKIPPED NONE` when nothing is skipped. Zero factories with `k = 0` → `TOTAL $0.00` /
`SKIPPED NONE`.

## Worked examples
```
# Part 1
FACTORIES
f1,0,100.00
f2,10,50.00
f3,25,80.00
PENALTIES
-->
TOTAL $230.00

# Part 2 (bands given out of order on purpose -- must sort by min_dist before use)
FACTORIES
f1,0,100.00
f2,10,50.00
f3,25,80.00
PENALTIES
16,inf,2.00
0,15,5.00
-->
TOTAL $240.00
   (pairs: dist(f1,f2)=10 -> band [0,15] -> $5.00 ; dist(f2,f3)=15 -> band [0,15] -> $5.00
    -> build 100+50+80=230.00, + 5.00 + 5.00 = 240.00)

# Part 2, a genuine gap
FACTORIES
f1,0,10.00
f2,12,10.00
PENALTIES
0,10,1.00
15,inf,1.00
-->
ERROR no penalty band for distance=12

# Part 3 -- both single-skip options happen to tie; smallest index wins
FACTORIES
f1,0,10.00
f2,12,10.00
f3,20,10.00
PENALTIES
0,10,1.00
15,inf,1.00
-->
TOTAL $21.00
SKIPPED f1
   (skip nothing: dist(f1,f2)=12 has no band -> invalid.
    skip f1 (j=0): only pair left is dist(f2,f3)=8 -> band [0,10] -> 10.00(f2)+10.00(f3)+1.00 = 21.00
    skip f2 (j=1): bridge dist(f1,f3)=20 -> band [15,inf] -> 10.00(f1)+10.00(f3)+1.00 = 21.00
    skip f3 (j=2): only pair left is dist(f1,f2)=12 -> no band -> invalid.
    skip f1 and skip f2 tie at $21.00 -> tie-break "smallest j" picks f1 (j=0) over f2 (j=1).)

# Part 4 -- k=2, the optimum needs to skip two NON-adjacent factories
FACTORIES
f1,0,10.00
f2,5,10.00
f3,9,10.00
f4,14,10.00
f5,20,10.00
PENALTIES
0,3,5.00
4,6,3.00
7,100,0.50
SKIP
2
-->
TOTAL $31.00
SKIPPED f2,f4
   (building all 5 costs 50.00 + four $3.00 adjacency penalties = 62.00. Skipping f2 and f4
    leaves f1(0), f3(9), f5(20) built: dist(f1,f3)=9 and dist(f3,f5)=11 both land in the cheap
    [7,100] -> $0.50 band, giving 30.00 + 0.50 + 0.50 = 31.00 -- cheaper than any single skip.)
```
The numbers above were produced by running `solution.py` on exactly this input (not computed by
hand and then transcribed) -- always cross-check a worked example against the reference solution
before trusting arithmetic written in a markdown file, this one included.

## Edge cases hidden tests are known to target
- Part 1: zero factories; a single factory; money strings with 0/1/2 decimal digits.
- Part 2: penalty bands listed out of `min_dist` order in the input; distance exactly on a band
  boundary (`min_dist` and `max_dist` both inclusive — test both edges of the same band); a gap
  with more than one affected pair (must report the **first**, i.e. smallest index, gap); a
  single factory (no pairs, never an error).
- Part 3: a case where "skip nothing" is already optimal (no skip beats every skip at equal or
  lower cost); a case where skipping the **first** or **last** factory (no bridge pair needed)
  is optimal; a case where two different single-skip options tie exactly and the smaller index
  wins; the "no valid configuration at all" error path.
- Part 4: `k = 0` behaves exactly like Part 2 (falls back to "skip nothing", still errors the
  same way Part 2 would on a gap); `k` large enough to skip every factory but one; a plan that
  needs to skip two **non-adjacent** factories to reach the optimum; the DP tie-break actually
  changing the reported `SKIPPED` list (construct two skip sets of equal total cost and confirm
  the documented tie-break, not just any valid one, is the one printed).
- Format: money always two decimals with a leading `$`; the three error strings match
  **verbatim** (`no penalty band for distance=<d>`, `no valid configuration`, `no valid
  configuration within skip budget k=<k>`); `SKIPPED` lists are comma-joined with no spaces, in
  corridor order, never sorted by id string.

## Variants seen in the wild
None known — this is a from-scratch reconstruction (see the confidence note above), not a
documented variant list from a real source.

## Sources
- `catalog/discovery/2026-09/C_batchA.md` `## C4 · Factory Cost` (2026-09-03 discovery pass;
  contains the PracHub / interviewdb / 1point3acres evidence table this problem is built from).
- https://prachub.com/interview-questions/minimize-total-factory-cost-with-distance-penalties
  (re-fetched 2026-09-03 while writing this problem: still only the one-sentence Quick Overview,
  no rules/format/examples behind it).
- https://www.interviewdb.io/question/stripe/factory-cost (title + stage confirmed, no body).
- https://www.1point3acres.com/interview/problems/post/7100090 ("Factory Cost Optimizer", title
  only — 1point3acres returns 403 to automated fetches).

## What this tests
skills: **A01** prefix sums + argmin with an explicit multi-level tie-break (Part 3's O(1)-per-
candidate skip evaluation) · **S06** integer minor-unit money, explicit "no rounding — reject
extra precision instead" rule · **S13** closed-interval band lookups, off-by-one at both
boundaries, first-gap-wins tie-break · **S08** deterministic ordering (Part 3/4's fully specified
multi-level tie-break rules, and `SKIPPED` output order) · plus the underlying DP itself (state
design, transition validity, and backtracking a reconstructed plan rather than just its cost) —
see the reconstruction-warning note above about not treating this as a documented real-world DP
pattern beyond that.
