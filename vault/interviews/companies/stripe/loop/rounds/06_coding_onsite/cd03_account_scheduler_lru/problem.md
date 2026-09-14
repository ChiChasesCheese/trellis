# cd03 · AccountScheduler — availability, timed locks, LRU auto-select (class API)

**Type:** onsite Programming Exercise · **Stage:** virtual onsite "general coding" (60 min, 3 part + follow-ups) · **Last asked:** 2026-03-27 (1point3acres 题库)
**Frequency:** 3 independent mentions (1point3acres 题库 "AccountScheduler LRU"; linkjob 2025-12-07/2026 onsite report "is_available / acquire(duration) / LRU auto-select"; process_and_jd.md onsite table) · **Confidence:** medium — the three-step progression (`is_available` → `acquire` → LRU auto-select) and method names are consistent across sources; the exact constructor shape, exception behaviour and the LRU tie-break rule are **reconstructed for this round** (marked below) and are a deliberate variant of `problems/q26_account_scheduler_lru` (which uses a `RELEASE`-having command-stream API with `add_account`/id-order tie-breaks): this round fixes the account pool at construction time, raises exceptions instead of returning sentinel booleans for unknown ids, and breaks LRU ties by **construction order** instead of id string order — do not reuse q26's solution verbatim, the contracts differ on purpose.

## Context
Stripe's test-mode tooling keeps a small, fixed pool of sandbox accounts that integration jobs
borrow for a while. A job asks whether one specific account is free, or locks it for `duration`
seconds, or just asks for *any* free account — in which case the scheduler hands out the
**least-recently-used** one so load spreads evenly and no single account gets hammered. The pool
of account ids is known up front (no dynamic `ADD`), which is what makes this a *class-design*
exercise rather than a stream-processing one: the interviewer wants to see clean state (one dict),
a defensible exception policy, and a straight line from "is it free" → "lock it" → "pick one for
me".

## Class API
```python
class AccountScheduler:
    def __init__(self, accounts: list[str]) -> None
    def is_available(self, account_id: str, t: int) -> bool
    def acquire(self, account_id: str, t: int, duration: int) -> bool
    def acquire_any(self, t: int, duration: int) -> str | None
```
`accounts` lists every valid id, in the order the caller cares about for LRU tie-breaking
(see Part 3). `t` and `duration` are plain integers (seconds); no currency, no floats anywhere.

## Rules
### Part 1 — registry and availability
Internal state is one dict, `locked_until: dict[str, int]`, initially empty (no entry = never
locked = available at every `t`). `is_available(account_id, t)` returns `True` iff
`account_id not in locked_until or t >= locked_until[account_id]` — i.e. a lock taken at `t0` for
`duration` covers `[t0, t0 + duration)`, an **exclusive end**: `is_available(id, t0+duration)` is
`True`, `is_available(id, t0+duration-1)` is `False`. Calling `is_available` (or `acquire`,
`acquire_any`) with an `account_id` that was not in the constructor's `accounts` list raises
`KeyError`.

### Part 2 — `acquire`: timed lock
`acquire(account_id, t, duration)` locks the account for `[t, t+duration)` and returns `True` if
it was available at `t`; otherwise it returns `False` and changes nothing. `duration <= 0` raises
`ValueError` **before** availability is even checked (a bad call is a bad call regardless of
state). A successful acquire sets `locked_until[account_id] = t + duration` and records
`last_used[account_id] = t` (used by Part 3). Unknown `account_id` raises `KeyError`, same as
Part 1, and takes priority over the `duration` check would only matter if both are wrong — the
reference solution validates `duration` first since it doesn't need to touch `locked_until` to do
so; either order is defensible, but the ordering must be picked and stated, not left to whichever
branch the interpreter hits first by accident. **Reference order: `duration` before unknown-id.**

### Part 3 — `acquire_any`: LRU auto-select
Among accounts available at `t` (per Part 1's rule), pick one and lock it exactly as `acquire`
would (same `duration <= 0` → `ValueError`), then return its id. Selection order:
1. **Never-acquired accounts first** — an account that has never had a *successful* `acquire`
   (Part 2 or a prior `acquire_any`) always outranks one that has, no matter how long ago.
2. Among never-acquired candidates, tie-break by **construction order** — the position of the id
   in the `accounts` list passed to `__init__`, **not** alphabetical order.
3. Among previously-acquired candidates, order by `last_used` **ascending** (oldest use wins);
   ties (equal `last_used`) also break by construction order.

If no account is available at `t`, return `None` and change nothing. A failed `is_available`
check, a failed `acquire`, or a plain `is_available` query never updates `last_used` — only a
*successful* lock does.

### `main()` — command stream
```
AVAIL <id> <t>            -> true | false | ERROR
ACQ <id> <t> <duration>   -> true | false | ERROR
ANY <t> <duration>        -> <id> | none | ERROR
```
The pool is fixed for the whole run: the **first line** is `ACCOUNTS <id1> <id2> ...` (space
separated, construction order = LRU tie-break order), all following lines are commands. Any
`KeyError`/`ValueError` raised by the class, any unknown verb, wrong arity, or non-integer
`t`/`duration` prints `ERROR` for that line and processing continues (this stream-level error
policy is a `main()`-only convenience — the class itself always raises, it never swallows).
Blank lines are ignored.

## Worked examples
```
ACCOUNTS a b
AVAIL a 0        -> true
ACQ a 0 10       -> true            (locks a: [0, 10))
AVAIL a 9        -> false
AVAIL a 10       -> true            (exclusive end)
ACQ a 5 5        -> false           (still locked at t=5)
ANY 5 10         -> b               (a locked; b never used)
ANY 5 10         -> none            (both now locked/unavailable)
ANY 15 5         -> a               (a free again at 15; last_used a=0 < b=5)
ACQ b 16 100     -> true
AVAIL b 17       -> false
ANY 20 1         -> a               (a: last_used=15; b: last_used=16 -> a older)
```
```
ACCOUNTS c b a
ANY 0 1          -> c               (all never used -> construction order c,b,a)
ANY 0 1          -> b
ANY 0 1          -> a
ANY 0 1          -> none            (all locked until 1)
ANY 1 1          -> c               (all free, last_used all 0 -> construction order again)
ACQ a 1 1        -> true            (a: last_used=1)
ANY 2 1          -> b               (last_used b=0 < c=a=1 -> LRU beats construction order)
```
```
ACCOUNTS x
ACQ x 0 0        -> ERROR           (duration <= 0 -> ValueError, caught by main())
AVAIL y 0        -> ERROR           (y unknown -> KeyError, caught by main())
ACQ x ten 5      -> ERROR           (non-integer t)
FROB x           -> ERROR           (unknown verb)
```

## Edge cases hidden tests are known to target
- exclusive lock end (`t0+duration` free, `t0+duration-1` not); re-lock exactly at expiry succeeds
- unknown `account_id` raises `KeyError` from `is_available`, `acquire`, and `acquire_any` alike
  when it's the caller's bug, not `main()`'s (the class never swallows — only `main()` does)
- `duration <= 0` raises `ValueError` from both `acquire` and `acquire_any`, even when no account
  would have been available anyway (validate before you look at state)
- LRU: never-used ranked before used, regardless of "how long ago" is meaningless for never-used
- never-used tie-break is **construction order**, not id string order (`ACCOUNTS c b a` yields
  `c, b, a`, not `a, b, c`) — this is the one place this round's contract diverges hardest from q26
- equal `last_used` among previously-used accounts also breaks by construction order
- failed `acquire` / plain `is_available` queries never touch `last_used`
- `acquire_any` when every account is locked -> `None`; after exactly one expires -> that one
- single-account pool; empty command stream; a pool where every account is used at t=0 (ties)
- non-monotonic `t` across calls (queries are answered purely by comparison against
  `locked_until`/`last_used`, never by "wall clock so far" — an earlier `t` after a later one
  must still be answered correctly)
- 10^5 commands over a pool of up to 10^4 accounts must run comfortably under budget

## Variants seen in the wild
- linkjob's wording implies an implicit clock (`now()` baked into the scheduler) instead of an
  explicit `t` argument on every call — same logic, inject the clock as a constructor default
  instead of a parameter; mention this as a live follow-up.
- `problems/q26_account_scheduler_lru` is the OA-flavoured sibling of this exact premise: dynamic
  `ADD`/`RELEASE`, boolean sentinels instead of exceptions, id-order LRU tie-break. Interviewers
  who ask for this shape in a 60-minute onsite tend to fix the pool and use exceptions instead —
  both are attested; this problem.md commits to the exception + fixed-pool + construction-order
  reading and says so explicitly rather than silently picking one.

## What this tests
skills: S03 class + dict modeling · S05 strict vs non-strict time comparisons · S08 deterministic
tie-breaks (construction order, not the "obvious" id order) · S10 state over an event stream ·
S18 validation/exception policy (raise vs return-sentinel, and which check runs first) ·
S19 incremental design (Part 1 → 2 → 3 each adding exactly one capability) · S20 self-testing

## Sources
- 1point3acres 题库 "AccountScheduler LRU" (onsite, last asked 2026-03-27) — `loop/raw/en_forums.md` §6.2 (C4 AccountScheduler)
- https://www.linkjob.ai/interview-questions/stripe-technical-interview/ (VO AccountScheduler — is_available / acquire(duration) / LRU auto-select)
- `loop/raw/en_forums.md` §6.2 lines ~276-277; cross-referenced against `problems/q26_account_scheduler_lru/problem.md` (sibling OA variant, explicitly NOT duplicated here — see Variants)

## 面试官会怎么追问
1. "如果要支持 `release(id)` 提前解锁,`last_used` 要不要跟着变?" — 期望候选人复述 q26 里已经验证过
   的答案:不变,因为"释放"不是"使用",提前释放的账户应该保留它原来的 LRU 位置,否则会被立刻选中
   造成"刚放出来又立刻抢回去"的抖动。
2. "10^5 次 `acquire_any` 调用,`accounts` 池有 10^4 个,现在这版是不是每次都要扫一遍?怎么优化到
   `O(log n)`?" — 期望候选人提出两个堆(free 堆 + locked 堆)+ 版本号懒删除,和 q26 的做法一致,并能
   讲清楚"锁刚好在这次调用之前过期"要怎么先把它挪回 free 堆。
3. "如果两次调用之间 `t` 反而变小了(时钟回拨),现在的实现还对吗?" — 正确答案是"对,因为状态判断
   全部基于存储的 `locked_until`/`last_used` 和传入的 `t` 直接比较,没有对'调用顺序=时间顺序'做
   任何假设";引导候选人现场证明这一点,而不是含糊带过。
4. "为什么未使用账户的 tie-break 是构造顺序,而不是 id 字符串顺序?这在生产环境里有什么意义?" —
   考察候选人是否理解"构造顺序"往往编码了业务优先级(比如账户池按可信度/容量排列),而不是随手选一
   个排序键;也是在检验候选人是否会照抄 q26 的 id-order 答案而不读题。
5. "多线程环境下多个 job 同时调 `acquire_any`,会不会两个线程选中同一个账户?怎么修?" — 期望候选人
   识别出"选择"和"加锁"必须是一个原子操作(读-判断-写的竞态),提出用一把锁包住整个
   `acquire_any` 方法体,或者用 CAS 风格的重试。
6. "为什么 `duration <= 0` 要在检查 unknown id 之前验证?如果反过来会有什么后果?" — 检验候选人是否
   真的对"校验顺序"这种细节做过取舍,而不是巧合地写对了;正确的讨论点是"两种顺序都能自洽,但必须
   写进文档并保持一致,不能一部分方法先查 id 一部分先查 duration"。
7. "如果账户池要支持运行时增删(变回 q26 那种 `ADD`),你的 Part 3 tie-break 还成立吗?" — 期望候选人
   意识到"构造顺序"在动态池下不再有意义,需要换成"首次注册顺序"这种新的单调递增序列(比如一个自增
   计数器),而不是死记当前的静态顺序。
