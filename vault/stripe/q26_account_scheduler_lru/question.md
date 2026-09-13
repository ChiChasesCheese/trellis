# q26 · AccountScheduler — availability, timed locks, LRU auto-select

## Context
Stripe's test-mode tooling keeps a pool of sandbox accounts that integration jobs borrow for a
while. A job asks whether a specific account is free, or locks it for `duration` seconds, or just
asks for *any* free account — in which case the scheduler hands out the **least recently used**
one so that load spreads evenly and no account is hammered. Locks expire on their own; a job may
also release early.

## Input (stdin) — one command per line, rules accumulate (no `PART` header)

| 格式 | 说明 |
|---|---|
| `ADD <id>` | register an account -> OK \| EXISTS |
| `AVAILABLE <id> <t>` | is it free at time t? -> true \| false |
| `ACQUIRE <id> <duration> <t>` | lock id for [t, t+duration) -> true \| false |
| `ACQUIRE_ANY <duration> <t>` | lock the LRU free account -> `<id>` \| NONE |
| `RELEASE <id>` | unlock now -> OK \| UNKNOWN |

`t` and `duration` are integers (seconds). Blank lines are ignored; anything else (unknown verb,
wrong arity, non-integer number) prints `ERROR` and changes nothing (Part 4). Timestamps are
usually non-decreasing but the solution must not depend on it: every query is answered for the
`t` it carries.

## Output
One line per command, in input order, exactly as in the table above.

## Class API (what the interviewer asks for; the command stream is a thin driver)
**AccountScheduler()**

| 格式 | 说明 |
|---|---|
| `add_account(id) -> bool` | True if new, False if it already existed (no change) |
| `is_available(id, t) -> bool` | False for unknown ids |
| `acquire(id, duration, t) -> bool` | lock [t, t + duration); False if unknown / locked / duration <= 0 |
| `acquire_any(duration, t) -> str \| None` | LRU free account, locks it and returns its id |
| `release(id) -> bool` | unlock immediately; False for unknown ids; idempotent |

## Rules
### Part 1 — registry and availability (`ADD`, `AVAILABLE`, `ACQUIRE`)
An account is **available at t** iff it is registered and not locked, or its lock ends at or
before `t`: a lock taken at `t0` for `d` covers `[t0, t0 + d)` — **exclusive end**, so
`is_available(id, t0 + d)` is `true` and `is_available(id, t0 + d − 1)` is `false`.
`acquire` succeeds only if the account is available at `t` and `duration > 0` (reconstructed);
success records `last_used = t`. Re-adding an existing id is a no-op (`EXISTS`).

### Part 2 — `ACQUIRE_ANY`: least-recently-used auto-select
Among accounts available at `t`, pick **never-acquired accounts first** (smallest id), otherwise
the smallest `last_used` (the `t` of its last successful acquire), ties by id (plain string
order). Lock it exactly as `acquire` would and print its id; print `NONE` if no account is
available or `duration <= 0`. Only successful acquires update `last_used`; failed `ACQUIRE`s,
`AVAILABLE` queries and `RELEASE` never do.

### Part 3 — `RELEASE`
`RELEASE id` clears the lock immediately (the account is available at every `t` until it is
acquired again). `last_used` is untouched, so an early-released account keeps its LRU position.
Releasing an unlocked account is a harmless `OK`; an unknown id prints `UNKNOWN`.

### Part 4 — stdin command stream with validation
`main()` processes the whole stream with one scheduler. Malformed lines print `ERROR`. The
solution must handle 10^5 commands over 10^4+ accounts: `ACQUIRE_ANY` should not scan every
account (heap keyed by `(never_used, last_used, id)` + a heap of locks keyed by `locked_until`,
with lazy invalidation); an O(n) scan is acceptable only for small pools — say so in comments.

## Worked examples
**Example 1 — locks, exclusive end, LRU**
```
ADD a               OK
ADD b               OK
ADD a               EXISTS
AVAILABLE a 0       true
ACQUIRE a 10 0      true
AVAILABLE a 9       false
AVAILABLE a 10      true
ACQUIRE a 5 5       false
ACQUIRE_ANY 10 5    b            (a is locked; b never used)
ACQUIRE_ANY 10 5    NONE
ACQUIRE_ANY 5 15    a            (both free; last_used a=0 < b=5)
ACQUIRE b 100 16    true
RELEASE b           OK
AVAILABLE b 17      true
ACQUIRE_ANY 1 20    a            (a free again at 20; last_used a=15 < b=16)
```
**Example 2 — never-used first, then ties by id, then LRU beats id order**
```
ADD c / ADD b / ADD a          OK OK OK
ACQUIRE_ANY 1 0                a      (all never used -> smallest id; a: last_used 0, locked [0,1))
ACQUIRE_ANY 1 0                b
ACQUIRE_ANY 1 0                c
ACQUIRE_ANY 1 0                NONE   (all locked until 1)
ACQUIRE_ANY 1 1                a      (all free, last_used all 0 -> id order; a: last_used 1)
ACQUIRE c 1 1                  true   (c: last_used 1)
ACQUIRE_ANY 1 2                b      (last_used b=0 < a=c=1 -> LRU rule beats id order)
```
**Example 3 — release and errors**
```
ADD x / ADD y            OK OK
ACQUIRE x 100 0          true
ACQUIRE y 100 0          true
ACQUIRE_ANY 1 50         NONE
RELEASE y                OK
ACQUIRE_ANY 1 50         y
AVAILABLE y 50           false
AVAILABLE y 51           true
RELEASE nope             UNKNOWN
ACQUIRE x 0 200          false     (duration must be > 0)
ACQUIRE x ten 200        ERROR
FROB x                   ERROR
```

## 关联知识点

- [[s03-small-record-modeling|S03 用小记录 + 按 id 索引的字典建模]]
- [[s05-threshold-semantics|S05 阈值语义：严格 vs 非严格、计数 vs 比例、最小量门槛]]
- [[s08-deterministic-sort-tiebreak|S08 确定性排序与完整 tie-break]]
- [[s10-event-stream-reversal|S10 事件流 + 反向事件]]
- [[s11-idempotency-dedup|S11 幂等 / 去重]]
- [[s18-validation-error-paths|S18 校验与错误路径]]
- [[s19-incremental-design-parse-model-compute-render|S19 增量式设计：parse → model → compute → render]]
- [[s20-self-test-discipline|S20 自测纪律]]
