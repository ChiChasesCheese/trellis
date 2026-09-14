# cd06 · Suspicious Users Sliding Window — O(n²) 朴素扫描 → O(n log n) 排序+双指针

**Type:** onsite Programming Exercise · **Stage:** virtual onsite "general coding" (60 min, 2 part + follow-ups) · **Last asked:** 2025-09-10 (Medium programhelp VO 写作)
**Frequency:** 1 mention, but with an almost-verbatim problem statement (rare for this repo's sources) · **Confidence:** high for the core rule ("more than 3 transactions in a 1-minute window", naive-then-optimized progression); the exact I/O protocol, the closed-interval window definition, the "first trigger" return shape for Part 2, and all worked numbers are this repo's reconstruction — the source is a one-paragraph interview-experience recap, not a problem spec (see Sources).

## Context
Stripe Radar flags a card as compromised or a merchant as running fraud when the same user fires
an unusually dense burst of transactions — say, more than 3 charges inside any rolling 60-second
window. The naive check (for every transaction, count how many of that user's other transactions
fall in the preceding minute) is O(n²) per user; the interview explicitly asks for the upgrade to
a sorted-timestamps + two-pointer scan, O(n log n) overall. Amounts and transaction order in the
input are noise — the only two Stripe payments idioms actually tested are "a window is defined by
its own trigger point, not by clock-aligned buckets" and "sort first, because production events
never arrive in order".

## Input (stdin)
First line `PART n` (n ∈ {1,2}). Then one transaction per line, `user_id,amount,timestamp`.
`amount` is a decimal-dollar string (parsed, but not used by either part's rule — see Variants for
a follow-up that does use it); `timestamp` is a **non-negative integer** number of seconds
(no unit conversion, no timezone). Blank lines are ignored. Rows may arrive **out of order**, both
across users and within a single user's own transactions — nothing about the input is presorted.
Up to 10^6 rows.

## Output
API: `part1(lines: list[str]) -> list[str]`, `part2(lines: list[str]) -> list[str]`. Only
suspicious users are printed — a user with no qualifying window contributes no output line at all
(this is a detector, not a per-user report card). Sorted by `user_id`, **plain string order**.
- **Part 1**: one line per suspicious user, just `user_id`.
- **Part 2**: one line per suspicious user,
  `user_id: <count> in [<start_ts>, <end_ts>]` — `count` is the transaction count in that user's
  **first-triggering** window (the earliest window, in time order, whose count first reaches the
  threshold), `start_ts`/`end_ts` are that window's closed bounds.

## Rules
### Window definition (both parts, fixed)
For a user's transaction at time `t`, its window is the **closed interval `[t-60, t]`** — 60
seconds looking backward from (and including) `t` itself, never centered and never forward-looking.
A transaction is "suspicious" if **any** of that user's own transactions `t` has **more than 3**
(i.e. **≥ 4**) of that same user's transactions — counting `t` itself — with timestamps inside
`[t-60, t]`. Two transactions at the exact same timestamp both count, and a window can collapse to
a single instant (`start_ts == end_ts`) when 4+ transactions share one timestamp.

### Part 1 — naive, per-user O(n²) (or better) is fine
For each user: for every transaction `t` belonging to that user, count how many of that user's
transactions (including `t`) fall in `[t-60, t]`; if any count reaches 4, the user is suspicious.
Output just the flagged `user_id`s.

### Part 2 — sorted two-pointer, O(n log n) overall, O(1) extra per user beyond the sort
Sort **all** rows by `(user_id, timestamp)` (ties broken by original input order — this never
changes which windows exist, since duplicate timestamps mean identical bounds either way, but it
keeps "first trigger" reproducible). For each user, walk a two-pointer scan over their
timestamp-sorted transactions: advance the left pointer past anything older than `t-60` as the
right pointer (t) advances; the **first** `t` (in ascending time order) at which the window count
first reaches 4 is the user's reported trigger — `start_ts` is the left pointer's timestamp,
`end_ts` is `t`, `count` is the window size at that moment. Report only that first trigger, never
a later or larger one.

## Worked examples
Shared input (deliberately scrambled — user grouping and per-user time order must not depend on
line order):
```
alice,10.00,1030
bob,5.00,2000
alice,12.00,1000
alice,8.00,1050
bob,5.00,2000
alice,9.00,1015
carol,1.00,3000
bob,5.00,2000
bob,5.00,2000
```
Grouped and time-sorted per user: alice = `1000, 1015, 1030, 1050` (then a later, unrelated
`1200` in a second example below); bob = `2000, 2000, 2000, 2000`; carol = `3000` (alone).

`PART 1` →
```
alice
bob
```
(alice: window ending at 1050 covers `[990, 1050]`, i.e. all of `1000,1015,1030,1050` since
`1050-1000=50 <= 60` — 4 transactions, suspicious. bob: all four transactions share `timestamp=2000`
→ window `[2000,2000]` trivially contains all 4. carol has only 1 transaction, never suspicious.)

`PART 2` →
```
alice: 4 in [1000, 1050]
bob: 4 in [2000, 2000]
```
(alice's first-triggering `t` is `1050` — at `t=1030` the window `[970,1030]` only has 3
transactions (`1000,1015,1030`), not yet suspicious; at `t=1050` it becomes 4. bob's first
trigger is already at the 4th record, `t=2000` — all 4 share one instant.)

A second example showing the *non*-triggering boundary and the ">3" threshold:
```
dave,1.00,0
dave,1.00,20
dave,1.00,40
dave,1.00,101
```
`dave`'s first three (`0,20,40`) span exactly 40s, only 3 transactions — not suspicious (need > 3,
not >= 3). The fourth, at `101`, is `101-0=101 > 60` from the first — no window ever contains all
four (widest 3-in-a-row window is still capped at 3). `dave` never appears in either part's output.

## Edge cases hidden tests are known to target
- exactly 3 transactions in any window → **not** suspicious (`> 3`, not `>= 3`)
- exactly 4 transactions with the two extremes exactly **60s apart** → suspicious (closed
  interval, inclusive boundary — `61s` apart excludes one and may drop below threshold)
- duplicate timestamps: several transactions sharing one `timestamp` all count individually
  toward the same window, and the window's `start_ts == end_ts` when they're the only ones in it
- a user with fewer than 4 total transactions is never suspicious — no windowing needed
- input rows out of order both **across** users and **within** one user's own transactions — the
  grouping/sorting step is mandatory, not an optimization
- empty input → empty output (no suspicious users) for both parts
- a user with two separate qualifying bursts (e.g. 4 close together early, another 4 close
  together much later) — Part 2 reports only the **first** (earliest-triggering) window, never the
  later one and never the largest one
- `PART 1` output is a bare `user_id`; `PART 2` output additionally reports the window and count —
  the two parts' formats are deliberately different, not a superset/subset of each other's fields
- large-scale: up to 10^6 rows, must run comfortably under the stated perf budget for Part 2
  (naive O(n²) Part 1 is not perf-tested at that scale — see the `perf` test's smaller bound)

## Variants seen in the wild
- The source's one-line recap ("more than 3 transactions in a 1-minute window") does not specify
  whether the window is trailing (anchored at each transaction, looking back), a fixed-size sliding
  buckets scheme, or a "does *some* 60s window exist" question independent of any anchor point —
  those three are mathematically equivalent for a *pure count* threshold (the maximum count over
  all trailing-anchored windows equals the maximum count over all possible 60s windows), so this
  repo picks the trailing/anchored formulation because it is the one that makes "first trigger" and
  its reported `[start_ts, end_ts]` well-defined and directly traceable to one real transaction.
- A natural real-world follow-up (not in the source, listed under 面试官会怎么追问) adds an amount
  condition: "more than 3 transactions **and** combined amount over $X" in the same window — this
  repo's `amount` field is deliberately present but unused in the core rule so that follow-up can
  be posed without changing the input format.

## What this tests
skills: S02 parsing (CSV, possibly out-of-order) · S04 grouping by key · S05 sliding-window / two-
pointer technique · S08 deterministic tie-break under sorting · S09 exact output formatting ·
S17 algorithmic complexity upgrade (O(n²) → O(n log n), stated and justified, not just coded) ·
S19 incremental design (Part 1 naive → Part 2 optimal, same detection rule)

## Sources
- https://medium.com/@neat_lava_bear_388/stripe-vo-interview-experience-interview-experience-coding-system-design-behavioral-a7bf34b1abcb
  (programhelp VO write-up, 2025-09-10: "Given a list of credit card transactions (user_id,
  amount, timestamp), detect suspicious users who have more than 3 transactions in a 1-minute
  window" — candidate reports solving it first O(n²), then with a hashmap+sliding window O(n)).
  See `loop/raw/en_forums.md` §6.2 C5 (line ~318).

## Clarifications (author's own, not sourced)
- The source gives the rule in one sentence and no I/O sample at all; the exact stdin/stdout
  protocol (`PART n` header, CSV row shape, the `user_id: count in [start, end]` format for
  Part 2, plain-string `user_id` sort) is this repo's own design, modelled on this suite's other
  `06_coding_onsite` problems' two-part dispatch convention.
- "1-minute window" is fixed here as the **closed** interval `[t-60, t]`, i.e. 61 possible integer
  offsets from 0 to 60 inclusive count as "within the minute" — the source does not specify open vs
  closed, and this repo picks closed because it makes the boundary case ("exactly 60s apart")
  decidable without guessing, and states it explicitly rather than leaving it implicit in the code.

## 面试官会怎么追问
1. "阈值 `> 3` 和窗口 `60s` 都改成参数会怎么样？" —— 期望候选人把 `part1`/`part2` 签名改成接受
   `min_count` / `window_seconds`（带默认值保持向后兼容），并指出双指针算法本身完全不用变，因为
   `> 60` 这一个比较就是唯一硬编码阈值的地方。
2. "现在只按笔数判断，如果要求窗口内**累计金额也超过 $X** 才算可疑呢？" —— 期望候选人认识到双指针
   仍然适用，但需要额外维护一个"窗口内金额之和"的运行量：右指针进入时加、左指针移出时减（前提是
   金额非负；如果允许退款/负数金额，简单的加减和就不再单调，需要退化成窗口内重新求和或换用支持
   区间和查询的结构）。
3. "如果交易是实时流进来的（在线场景），而不是一次性给你整个列表，你怎么做？" —— 期望候选人提出
   每用户维护一个 `deque[timestamp]`：新事件来了 append，同时从队首弹出所有 `< t-60` 的旧时间戳，
   队列长度就是当前窗口计数，均摊 O(1) 每事件，不需要整体排序。
4. "10^6 笔交易、但可能有 10^5 个不同用户，且大部分用户只有一两笔——内存上限怎么控制？" —— 期望
   候选人提出"低活跃度用户不需要一直占内存"：流式场景下用一个按最后活跃时间排序的结构（如
   `OrderedDict` 或最小堆）定期淘汰长期不活跃的用户队列，而不是无限期为每个 user_id 保留一个 deque。
5. "`timestamp` 如果跨天、跨时区，还是纯 epoch 秒吗？如果客户端本地时间戳且各自时区不同呢？" ——
   期望候选人指出本题用整数 epoch 秒从根本上绕开了 DST/时区问题（epoch 是全局单调的），一旦换成
   "本地墙钟时间字符串"就必须先统一转成 UTC 再比较，否则窗口边界会因跨时区用户而出现虚假触发或漏报。
6. "题目里没有交易 id，如果同一笔交易因为重试被发送了两次（内容完全相同，包括 timestamp），你的
   算法会把它算成两笔，从而制造假阳性——怎么办？" —— 期望候选人提出给输入 schema 加一个交易 id，
   在分组排序之前先按 id 去重（或用一个短 TTL 的去重缓存应对流式场景），并明确指出"现在这版协议
   没有 id 字段，所以没法在当前实现里真正做到"，展示候选人分得清"协议限制"和"算法限制"。
7. "两个用户在完全相同的时刻各自触发了自己的第一个窗口，'先触发的用户'这个说法有意义吗？" ——
   期望候选人指出"first trigger"是**逐用户独立定义**的（每个用户的第一个满足条件的窗口，与其他
   用户无关，也不存在跨用户的先后比较），本题输出本来就与"哪个用户先触发"无关，只与"每个用户
   自己最早触发的窗口是哪个"有关，避免被这个措辞带偏。
