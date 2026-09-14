# cd04 · Rate Limiter (4-part) — basics, memory, tricky edges, threads

**Type:** onsite Programming Exercise · **Stage:** virtual onsite "Programming Exercise" (60 min, 4 part) · **Last asked:** 2026-09-01 (1point3acres 题库, TOC-only, curled)
**Frequency:** 1 independent mention with a concrete 4-part TOC (1point3acres 题库 "Rate Limiter": Part 1 The Basics → Part 2 Saving Memory → Part 3 Tricky Situations → Part 4 Handling Multiple Threads); cross-referenced against the same repo's `problems/q23_rate_limiter/problem.md` (a *different*, better-sourced OA rate-limiter with 8 independent mentions) for realistic numbers and boundary conventions · **Confidence:** low-medium — the 4-part *structure* (basics → memory → edges → concurrency) is directly sourced from a curled TOC (only the section titles were readable, not the body); every numeric example, the memory-analysis requirement, the specific "tricky situations" list, and the threading contract in this problem.md are **reconstructed** to be internally consistent with that TOC and with q23's established conventions (window boundary, "denied requests aren't recorded"). This is a deliberately different exercise from q23: q23 is sliding-window / per-client / weighted / token-bucket (OA-flavoured, "add a feature per part"); this one is "make the same simple rate limiter production-grade" (OA-flavoured but the four parts are basics → memory → edge cases → concurrency, not new algorithms) — do not copy q23's solution, the part boundaries and the class shape differ.

## Context
Every Stripe API key is rate limited. The onsite version of this exercise, per the 1point3acres
TOC, doesn't ask you to invent a new algorithm each part (that's q23) — it asks you to take the
*simplest possible* correct rate limiter and push it toward something you'd actually deploy: first
make it correct, then make it not leak memory, then handle the edge cases a naive implementation
gets wrong, then make it safe under real concurrent traffic. This progression — "basics → memory →
edge cases → threads" — is the recurring Stripe onsite template also seen in the transaction-level
and account-scheduler problems in this round.

## Class API
```python
class RateLimiter:
    def __init__(self, limit: int, window_s: int) -> None
    def allow(self, client_id: str, t: int) -> bool
    def evict_idle(self, now: int) -> int
    def log_size(self, client_id: str) -> int      # observability hook, see below
```
`log_size(client_id)` returns the number of timestamps currently retained **in memory** for that
client (0 for an unknown/never-seen/evicted client) — it exists purely so Part 2's memory-bound
claim (`O(limit)` per active client) can be asserted directly in tests instead of only inferred
from behaviour, and is the one method whose whole reason to exist is testability, not the
production contract; say this out loud if an interviewer asks "why is this here."
`limit` is the maximum number of allowed requests per client per window. `window_s` is the window
length **in seconds**; internally everything is converted to and compared in **milliseconds**
(`window_ms = window_s * 1000`) because `t`, the timestamp argument to every call, is an integer
**millisecond** timestamp — this is pinned here explicitly because "is `t` seconds or ms" is the
single most common silent-bug source in every rate-limiter writeup this repo has seen; this
problem commits to milliseconds and says so in every method's docstring.

## Rules
### Part 1 — the basics: a correct sliding-window log
Per client, keep a log of the timestamps of every **allowed** request. `allow(client_id, t)` is
`True` iff the number of entries in that client's log with timestamp in the **left-open,
right-closed window `(t - window_ms, t]`** is `< limit` (same boundary convention as
`problems/q23_rate_limiter`, for consistency across this repo) — i.e. allow iff `count + 1 <=
limit`. A denied request is **never added to the log** (a burst of denials must not itself count
against the limit, and must not extend anyone's lockout). A first-cut implementation may keep
every timestamp ever seen in an unbounded `list` and re-scan it on every call — this is correct
but **unbounded in memory and O(n) per call**; that's exactly the problem Part 2 exists to fix.

### Part 2 — saving memory: bounded log + idle client eviction
Two independent memory leaks exist in the Part 1 sketch, and both must be closed:
1. **Per-client log growth.** Replace the raw list with a `collections.deque`, and on every call
   pop expired entries (`<= t - window_ms`) off the **left** before counting/appending. Because
   denied requests are never appended, a client's deque can never hold more than `limit` entries
   — memory per *active* client is `O(limit)`, not `O(total requests ever made)`.
2. **Dead client accumulation.** A client who made exactly one request and never returns still has
   an entry in the outer `dict` forever. Add `evict_idle(now: int) -> int`: for every client, trim
   its deque against `now` the same way `allow` would, and if the deque is now **empty** (i.e. the
   client made no request in `(now - window_ms, now]`), drop the client entirely from all internal
   state. Return the number of clients evicted. Calling `evict_idle` periodically (e.g. once per
   window) bounds total memory to `O(limit × A)` where `A` is the number of clients active in the
   trailing window — never `O(limit × every client that ever connected)`.

### Part 3 — tricky situations (definitively pinned, not left as "undefined behaviour")
- **Clock going backward.** If `t` for a given `client_id` is smaller than the last `t` **ever
  passed for that client** (allowed or denied), the call is **not rejected** — it is **clamped
  forward** to that client's last-seen `t` before anything else happens (window check, log
  trimming, log append all use the clamped value). Rationale stated for the interview: a
  `ValueError` on backward clock would make the limiter itself a source of production incidents
  every time NTP skews two collectors; clamping degrades gracefully to "treat it as arriving now"
  instead. This also keeps each client's internal deque monotonically non-decreasing, which the
  Part 2 trimming logic assumes.
- **`limit == 0`.** Always deny, unconditionally, for every `client_id`, forever. No `ValueError`
  — a limiter configured with zero capacity is a valid (if useless) configuration, e.g. an
  operator killing a misbehaving key's traffic entirely.
- **A burst of simultaneous requests (`t` identical across many calls).** Handled by the ordinary
  rule: the window `(t - window_ms, t]` includes `t` itself, so of `k` calls at the same `t`,
  exactly `min(k, remaining capacity)` are allowed, evaluated **in call order** — ties are not a
  special case, they fall out of the Part 1 rule for free.
- **`client_id == ""`.** The empty string is a valid dictionary key like any other; it identifies
  "the anonymous client" and gets its own independent budget. No special-casing at the class level
  — this is tested against `RateLimiter.allow` directly, not through `main()`'s `ALLOW` command,
  because the stream format tokenizes on whitespace-split and cannot represent an empty token as a
  distinct field from "no field at all" (`"ALLOW  100".split()` silently collapses to two tokens);
  that's a limitation of the line-oriented `main()` protocol, not of the class.
- **Very large `t`** (e.g. `10**15`, comparable to a plausible far-future millisecond timestamp,
  or truly enormous synthetic values). Python integers do not overflow; a naive fixed-size counter
  language would need to check this explicitly, and that's worth saying out loud in the interview
  even though Python sidesteps it.

### Part 4 — multiple threads
`allow` and `evict_idle` must be safe to call concurrently from multiple threads against the
**same** `RateLimiter` instance, with `allow` remaining **exact** (not eventually-consistent, not
approximate) — if `limit` requests are legally allowed in a window, concurrent callers must
collectively see exactly `limit` `True`s, never more (a race would double-book capacity) and,
given enough concurrent attempts, never fewer either. The reference solution wraps the whole
critical section (read log, trim, count, decide, append) of both `allow` and `evict_idle` in one
`threading.Lock` held for the instance's lifetime — see REPORT.md for the discussion of a
per-client-lock alternative and why it isn't worth the extra complexity at this problem's scale.

## Worked examples
```
RateLimiter(limit=3, window_s=1)     # window_ms = 1000
allow("u", 0)    -> True    (log: [0])
allow("u", 100)  -> True    (log: [0, 100])
allow("u", 200)  -> True    (log: [0, 100, 200]; count was 2 < 3)
allow("u", 300)  -> False   (window (-700, 300] holds 0,100,200 -> count 3, not < 3; log unchanged)
allow("u", 1000) -> True    (window (0, 1000]; the entry at t=0 is now excluded (left-open) ->
                              count 2 < 3; log: [100, 200, 1000])
```
```
RateLimiter(limit=2, window_s=60)                 # window_ms = 60000
evict_idle(now=0)              -> 0               # no clients yet
allow("a", 0)                  -> True
allow("b", 0)                  -> True
evict_idle(now=59999)          -> 0                # both still in window (0, 59999]
evict_idle(now=60000)          -> 2                # window is now (0, 60000]; entry at t=0 is EXCLUDED
                                                     # (left-open) -> both deques empty -> both evicted
allow("a", 60000)              -> True              # "a" was evicted, comes back with a fresh budget
```
```
RateLimiter(limit=1, window_s=1)          # window_ms = 1000
allow("c", 500)  -> True     (log: [500])
allow("c", 300)  -> False    (t=300 < last-seen 500 -> clamped to 500; window (-500, 500] already
                               holds the entry at 500 -> count 1 == limit -> DENIED; log unchanged)
allow("c", 1500) -> True     (real time now advances past the clamp; window (500, 1500] excludes
                               the entry at t=500 (left-open) -> count 0 < 1 -> True; log: [1500])
```

## Edge cases hidden tests are known to target
- window boundary: `t - window_ms` excluded, `t` included (mirrors q23's convention exactly)
- a denied request must not be appended to the log (a burst of denials must not extend anyone's
  effective lockout, and must not itself ever "expire" since it was never recorded)
- Part 2: after many denied calls interleaved with allowed ones, a client's deque never exceeds
  `limit` entries — assert this directly by inspecting internal state size, not just behavior
- Part 2: `evict_idle` removes exactly the clients whose window is empty as of `now` (boundary
  `==` evicts, one ms before does not), and returns the exact count; an evicted client that
  returns later gets a fresh, full budget (its old history is gone, not "remembered")
- Part 3: `t` smaller than a client's last-seen `t` is clamped, not rejected, and the clamp is
  **per-client** (client A's backward jump does not affect client B's clock)
- Part 3: `limit == 0` denies every call, immediately, with no exception
- Part 3: many calls at the identical `t` — exactly `limit` succeed, deterministic call order
- Part 3: `client_id == ""` behaves like any other client, independent budget
- Part 3: `t` at `10**15` scale does not crash or misbehave
- Part 4: 8 threads × 1000 concurrent `allow()` calls against one shared client / one shared
  window must yield **exactly** `limit` `True`s — not "approximately", not "usually" — asserted
  with an exact equality, proving the critical section is genuinely atomic under contention
- 10^5 sequential `allow()` calls across many clients must run comfortably under budget

## Variants seen in the wild
- The source TOC's "Saving Memory" section is consistent with the generic pattern (seen across
  many rate-limiter writeups, not Stripe-specific) of contrasting a naive full-history log against
  a trimmed sliding-window log; an accepted alternative **not implemented here** (put in the
  follow-ups) is an *approximate* sliding window: `previous_window_count × overlap_fraction +
  current_window_count`, which trades exactness for O(1) memory per client (no per-request log at
  all) — mention this trade-off if asked "how would you save even more memory."
- `problems/q23_rate_limiter` is this repo's other rate-limiter problem: sliding window (global →
  per-client → weighted) plus a token bucket, with its own `SlidingWindow`/`RateLimiter`/
  `TokenBucket` classes and a `CLEANUP` stream command. That problem's "memory cleanup of idle
  keys" follow-up is the same idea as this problem's Part 2 `evict_idle`, independently attested —
  cross-reference, don't merge; the two problems' class shapes and part boundaries are different
  on purpose (this one has no per-client weight, no token bucket, and adds threading as its own
  part instead of a follow-up discussion).

## What this tests
skills: S03 modelling (state per client) · S05 strict vs non-strict window boundaries ·
S12 time windows · S16 sliding-window log · S17 memory-bound analysis (stating and proving an
`O(limit × A)` bound, not just writing code) · S18 validation / graceful-degradation policy
(clamp vs raise) · S19 incremental design · S21 stdlib fluency (`collections.deque`,
`threading.Lock`) · A15 thread-safety under contention (exact, not approximate, correctness)

## Sources
- 一亩三分地题库 "Rate Limiter" TOC (`loop/raw/cn_forums.md` line ~108): "题目是'设计并实现一个能
  跟踪 API 访问模式、强制请求限流的 rate limiter'，文章按 4 个 part 递进：Part 1 The Basics → Part 2
  Saving Memory → Part 3 Tricky Situations → Part 4 Handling Multiple Threads" — TOC only, body
  behind a login wall; every numeric example and rule in this problem.md is a reconstruction
  consistent with that TOC, not sourced numbers.
- `loop/raw/en_forums.md` §6.2 (C8, rate limiter mention in the onsite coding section) — cross-
  referenced for the "45-60 min, 2-4 part, add complexity per part" onsite template this exercise
  follows.
- `problems/q23_rate_limiter/problem.md` — this repo's better-sourced sliding-window/token-bucket
  rate limiter; used here only for the window-boundary convention (left-open, right-closed) and
  the "denied requests aren't recorded" rule, kept identical across both problems for consistency,
  **not** for its part structure or class shape, which this problem deliberately does not copy.

## 面试官会怎么追问
1. "Part 1 的实现每次 `allow` 都要重新扫一遍这个 client 的全部历史吗?复杂度是多少?" — 逼你先说出
   朴素版本是 `O(n)` 每次调用、且内存无上界,而不是一上来就写"优化版"蒙混过关;这正是 Part 2 存在
   的理由,面试官想看你能不能自己说出这个动机,而不是背答案。
2. "你说 `evict_idle` 把内存上界从'历史上出现过的所有 client'降到'当前活跃的 client',那这个上界的
   数学表达式是什么?" — 期望候选人现场写出 `O(limit × A)`(`A` = 活跃 client 数),并解释为什么
   `evict_idle` 必须被**定期调用**才有意义——它自己不是被动触发的。
3. "时钟回拨你选择 clamp 而不是抛异常,如果反过来 Stripe 要求'必须拒绝任何回拨的请求',你的实现要
   改哪几行?对 `deque` 的'单调递增'假设有什么影响?" — 检验候选人是否真的理解 clamp 存在的原因
   (维护 deque 单调性),而不是随手选了一个分支。
4. "`limit=0` 为什么不抛异常,而 Part 1 的 `window_s` 或者 `limit` 为负数呢?" — 一个开放追问,期望
   候选人现场做出并说明一个新的、内部一致的选择(比如构造时校验 `limit < 0` / `window_s <= 0` 抛
   `ValueError`,因为那是配置错误而非运行时正常状态,而 `limit == 0` 是合法配置),而不是照搬 `==0`
   的处理方式去处理负数。
5. "Part 4 你用一把全局锁包住整个 `allow`,如果 QPS 极高、client 数量巨大,锁竞争会不会成为瓶颈?
   怎么优化成 per-client 锁?" — 期望候选人提出"每个 client 一把锁 + 一把额外的锁保护外层 dict 的
   创建/删除(或者用 `defaultdict` + 只读升级为写锁的双重检查)",并能说清楚这比全局锁复杂在哪、
   何时才值得付出这个复杂度。
6. "为什么 8 线程 × 1000 次并发的测试断言的是'恰好等于 limit',而不是'大约等于 limit'?这在验证
   什么?" — 检验候选人是否理解"exact"这个词在并发正确性测试里的分量——它在证明临界区真的是原子
   的,而不是"大部分时候没有明显的竞态"这种弱得多的保证。
7. "如果这是分布式部署,多个进程/机器共享同一个 rate limit 预算,你的内存内 `deque` + `Lock` 方案
   还成立吗?要改成什么?" — 期望候选人提到 Redis + Lua 脚本(或等价的原子操作)做跨进程的滑动窗口
   计数,并能指出'进程内锁'和'分布式协调'是两个完全不同量级的问题。
