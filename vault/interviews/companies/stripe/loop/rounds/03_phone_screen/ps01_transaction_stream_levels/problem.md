# ps01 · Transaction Stream Levels — per-user totals → 60s sliding window → top-K → pattern detection

**Type:** phone screen (unlock-next-part) · **Stage:** Technical Phone Screen / Team Screen (45–50 min) · **Last asked:** 2025-10-25 (learncswithus.com) · **Frequency:** 1 detailed write-up (four-level breakdown, all four levels described independently) · **Confidence:** medium (single primary source with concrete Level-1/Level-3 examples; Level 2/4 descriptions are prose-only, no numeric example — this problem.md's worked examples for those two levels are reconstructed and clearly marked)

## Context
A stream of Stripe transactions (`user_id, amount, timestamp`) arrives, possibly out of order.
The interview is four independent "levels" on the same data shape, each unlocking after the
previous one passes: (1) aggregate totals, (2) flag users who transact fast enough to blow past
a threshold in any rolling minute, (3) find who's "hottest" right now, (4) spot a
small→large→small spending pattern. This is the shape of Stripe's real-time fraud/velocity
monitoring reduced to an interview-sized exercise — no persistence, no currency formatting
(amounts are plain integers; ps02 covers money formatting).

## Input (stdin)
```
PART n
<params line — present only for Part 2/3/4, see below>
user_id,amount,timestamp
user_id,amount,timestamp
...
```
* `PART n` — `n` ∈ {1,2,3,4}.
* **Params line**: a params line has **no comma** and at least one `key=value` token
  (space-separated, e.g. `T=100 W=60`); a data line always has **exactly two commas**. The
  parser uses this to distinguish them — if the line right after `PART n` has no comma and
  contains `=`, it is consumed as params; otherwise it's already the first data line (this is
  how Part 1, which needs no params, "just works" with no params line at all).
  - Part 2: `T=<int> W=<int>` — `W` defaults to `60` if omitted.
  - Part 3: `t=<int> K=<int>` — window is **fixed at 60s**, not a parameter.
  - Part 4: `S=<int>` — the small/large split point.
* `amount` is a non-negative integer (plain count/minor-unit-agnostic — no `$` formatting in
  this problem). `timestamp` is an integer number of seconds, **may arrive out of order**; all
  parts process transactions in timestamp order, tie-broken by **input order** (Python's stable
  sort — first-seen-first, standard practice: don't invent a second sort key when one isn't
  given). Up to 10^5 lines.
* Blank lines are ignored; fields tolerate surrounding whitespace.

## Output
Depends on part — see Rules below. All listings are sorted by `user_id` in **plain string
order** (`B` < `a`, `user10` < `user2`), matching the OA convention.

## Rules

### Part 1 — per-user totals
`{user_id: sum of amount}`, one line `user_id: total` per user that appears **anywhere** in the
input, sorted by `user_id`. Order-independent (sum is commutative) — this is the only part that
does not care about timestamp order.

### Part 2 — 60s sliding-window threshold
For each user independently, walk their transactions **in timestamp order**, maintaining a
deque of "still in window" `(timestamp, amount)` pairs. The window at the moment of transaction
with timestamp `ts` is the **closed interval `[ts - W, ts]`** (both ends inclusive — a
transaction exactly `W` seconds earlier is still counted; this is pinned by the Part 3 worked
example below, which only matches under a closed interval). If the running window sum reaches
`>= T` at any point, the user is flagged. Output `user_id: sum` for every flagged user, where
`sum` is the window total **at the first moment** (in timestamp order) the threshold was
crossed. Users never flagged are omitted (no `$0.00`-style universal listing here — Part 2 is a
"which users tripped the alarm" report, not a full ledger).

### Part 3 — top K by trailing-60s sum at time t
Sum each user's `amount` over transactions with `timestamp` in the closed interval
`[t - 60, t]` (fixed 60s window, not configurable). Only users with **at least one** transaction
in that window are candidates — there is no zero-padding for users who simply weren't active.
Rank candidates by `sum` **descending**; tie-break by `user_id` **ascending** (ties by amount are
possible and must be deterministic). Output the top `K` as `user_id: sum`, one per line, in
ranked order (**not** re-sorted by `user_id` — rank order is the whole point of this part). If
fewer than `K` users qualify, output all of them (no error, no padding).
*Implementation note (put this in the interview, it's a real trade-off): a single pass with a
dict + `sorted()` is `O(n + m log m)` (`m` = distinct users in window) and is what the reference
solution does; a size-`K` min-heap gets you `O(n log K)` and matters once `K << m` at real
scale — mention both, justify picking the simpler one for `n, m` this small.*

### Part 4 — `[small, large, small]` pattern detection
Classify each transaction by the single threshold `S`: `small` if `amount < S`, `large` if
`amount >= S`. For each user, walk their timestamp-ordered transactions and check **every
window of 3 consecutive transactions** (indices `i, i+1, i+2` for every valid `i`) — overlapping
matches all count independently (a run like `small, large, small, large, small` yields two
matches, at indices 0 and 2, not one). For each match, record the timestamp of the **first**
transaction in the triple. Output `user_id: t1,t2,...` (start timestamps, ascending) for every
user with **at least one** match; users with zero matches are omitted entirely.

## Worked examples
```
# Part 1 (learncswithus.com Level 1, verbatim: user,amount pairs, timestamps added since the
# source example predates timestamps — order doesn't matter for Part 1 anyway)
1,10,100
2,5,101
1,7,102
--PART 1-->
1: 17
2: 5

# Part 3 (learncswithus.com Level 3, verbatim tuples (user,amount,ts); t=90, K=2)
1,50,10
1,60,40
2,80,30
3,30,40
2,50,90
--PART 3 (t=90 K=2)-->
2: 130
1: 60
# window = [30,90]: user1 gets ts=40 (60) -> 60; user2 gets ts=30 (80) + ts=90 (50) -> 130;
# user3 gets ts=40 (30) -> 30 (not in top 2). This numeric result is what pins the window to
# CLOSED [t-60,t]: a half-open (t-60,t] window would exclude ts=30 and change the ranking.

# Part 2 (reconstructed — source gives no numbers, only "flag users who cross T within any
# 60s window"): T=100, W=60
u1,40,0
u1,40,30
u1,40,60
u2,200,5
--PART 2-->
u1: 120
u2: 200
# u1: at ts=60 the window [0,60] holds all three 40s -> sum 120 >= 100 (first crossing).
# u2: single transaction of 200 >= 100 immediately.

# Part 4 (reconstructed — source gives no numbers, only "detect [small,large,small], state
# machine"): S=50
u1,10,1
u1,60,2
u1,20,3
u1,70,4
u1,5,5
--PART 4-->
u1: 1,3
# labels: small,large,small,large,small -> triple (1,2,3)=s,l,s matches (start ts=1);
# triple (2,3,4)=l,s,l does not; triple (3,4,5)=s,l,s matches (start ts=3).
```

## Edge cases hidden tests are known to target
- Part 1: user with a single transaction; duplicate `user_id` rows; zero-amount transactions.
- Part 2: window boundary exactly `= W` seconds old (included) vs `W + 1` (excluded, first
  boundary test above proves this both ways); a user who never crosses `T` (omitted, not
  `0`-flagged); `W` omitted from the params line (defaults to 60).
- Part 3: boundary transaction exactly at `t - 60` (included) vs `t - 61` (excluded); a tie in
  `sum` between two users (broken by `user_id` ascending); fewer qualifying users than `K`
  (output truncates, no padding); `K = 0` (empty output).
- Part 4: overlapping matches (`s,l,s,l,s` -> two matches, not one, not zero); fewer than 3
  transactions for a user (no matches possible); a run of `large` amounts only (no matches);
  amount exactly `== S` counts as `large` (`small < S <= large`, strict `<` for small).
- All parts: out-of-order input lines (timestamps not in file order) must still process
  correctly; ties in `timestamp` fall back to input order (stable sort), not `user_id` or
  `amount`; `user_id` sort is plain string order (`B` < `a`, `user10` < `user2`); very large
  amount sums (10^9-scale) must stay exact integers.
- Performance: 10^5 lines across a few thousand distinct users must run comfortably under the
  perf budget for every part (dict + deque + sort are all near-linear here).

## Variants seen in the wild
- The source explicitly frames Level 3 as "MinHeap" — a heap-based top-K is an accepted
  alternative implementation to the dict+sort approach here; complexity trade-off is `O(n log K)`
  vs `O(n + m log m)`. Mention this as a live follow-up rather than a required implementation.
- Level 4 is described as "state machine, three-phase transition" — the triple-window scan here
  *is* a 3-state machine unrolled; an interviewer may ask you to implement it explicitly as
  `state ∈ {NEED_SMALL, NEED_LARGE, NEED_SMALL2}` per user instead of index-based triples.

## Sources
- https://learncswithus.com/2025/10/25/stripe-tech-screen/ (Stripe Technical Screen｜四个Level全解析, 2025-10-25) — primary source for all four levels; Level 1 and Level 3 include concrete numeric examples (reproduced above verbatim), Level 2 and Level 4 are prose-only descriptions (this problem.md's Level 2/4 worked examples and the closed-interval window boundary rule are reconstructions, not sourced numbers).
- `loop/raw/cn_forums.md` lines 43–56 (aggregated summary of the above, cross-referenced against `en_forums.md` P3.4 "parts are connected" phone-screen format description).

## What this tests
skills: S02 parsing (params-line vs data-line disambiguation) · S03 out-of-order stream
processing (sort-by-timestamp with stable tie-break) · S04 per-user grouping · S05 sliding
window (deque, closed-interval boundary) · S08 deterministic sort/tie-break (top-K ranking) ·
S09 exact formatting · S19 incremental design (state carried/reused across levels 2→3→4 via
the shared `_by_user_sorted` helper)

## 面试官会怎么追问
1. "如果同一用户在同一秒有 10 笔交易,Part 2/Part 4 的 tie-break 规则是什么?" — 追问是否真的理解
   "稳定排序 = 保留输入顺序"这条隐含契约,还是随手写了个 `sorted(key=ts)` 就当过关。
2. "Part 3 的窗口如果不是闭区间,而是 `(t-60, t]` 或 `[t-60, t)`,worked example 的排名会变吗?"
   — 逼你现场推导出闭区间是唯一能重现 `[2,1]` 输出的选择,而不是背答案。
3. "Part 2 如果不是'首次触发即报告',而要求'报告触发时刻窗口内的最大值'(可能不是首次触发),
   代码要怎么改?" — 考察对"首次 vs 最大值"这两种截然不同语义的隔离设计能力。
4. "数据量到 10^7 行、用户数到 10^6,Part 3 还能用 `sorted()` 吗?" — 期望候选人主动提堆
   (`heapq.nlargest` 或维护 size-K 最小堆),并能说清楚 `O(n log K)` vs `O(n + m log m)` 何时更优。
5. "Part 4 如果模式变成可配置长度(比如 `[small, large, small, large]`),你的实现要改多少行?"
   — 检验是否用了硬编码的三重判断,还是用了可扩展的 labels 数组 + 滑动比较。
6. "如果 timestamp 可能是负数(比如相对某个纪元的偏移),现在的实现还成立吗?" — 纯粹的边界/假设
   检查,答案应该是"成立,因为窗口比较全程用整数减法,没有对 timestamp 做非负假设"。
7. "如果输入是无限流(不能一次性读进内存),Part 1/Part 2 要怎么改成流式处理?" — Part 1 天然可以
   (在线累加字典);Part 2 每用户的 deque 本来就是流式的;引导候选人意识到当前实现已经很接近流式,
   只是被"先读完整个 stdin"这个 I/O 边界掩盖了。
