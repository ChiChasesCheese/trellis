# q11 · Subscription Database — start / end / check with durations that replace, then accumulate

## Context
Stripe Billing keeps a tiny "subscription database" per customer: a subscription `start`s (optionally for a
fixed number of time units), may be `end`ed (canceled) early, and support tooling asks "is this customer
`active` right now?". Real subscriptions renew — a renewal *extends* the current period rather than
restarting it — so the third part switches the semantics from "a new start replaces the old one" to
"a new start accumulates on top of the current expiry".

## Input (stdin)
First line `PART n` (n ∈ {1,2,3}); then one event per line, `timestamp,op,user[,duration]`.
`timestamp` and `duration` are non-negative integers; `op ∈ {start, end, check}`; `user` is a
case-sensitive string. `duration` may only appear on `start` (Parts 2–3). Blank lines and spaces around
commas are ignored. **Events are processed in the order given** (they are *not* re-sorted by timestamp;
the sources' samples are already chronological). Up to 2·10^5 lines.

## Output
One line per `check` event, **in input order**: `active` or `inactive`. `start` and `end` print nothing.
No output if there are no checks.

## Rules
### Part 1 — unlimited subscriptions
`t,start,user` makes `user` subscribed from `t` onward. `t,end,user` cancels it (no-op if the user is not
subscribed). `t,check,user` prints `active` if the user has an un-ended subscription, else `inactive`.
A check before any start, or after an `end`, is `inactive`. Same-timestamp events take effect in input
order (`5,start,A` then `5,check,A` → `active`; `5,end,A` then `5,check,A` → `inactive`).

### Part 2 — durations; a new start REPLACES the old subscription
`t,start,user,d` is active for every check time `c` with **`c ≤ t + d` (inclusive)**; from `t + d + 1` it is
expired. Source sample: `1,start,Michael,9` → active at 10, inactive at 11. A start without a duration is
unlimited. **Any new `start` replaces whatever the user had** (a finite one replaces an unlimited one and
vice versa; the old expiry is forgotten). `end` cancels regardless of remaining time. `d = 0` → active at
`t` only.

### Part 3 — durations ACCUMULATE
Same input as Part 2, but a `start` with duration `d` for a user whose subscription is **still active at
that start's timestamp** *extends* it: `new_expiry = current_expiry + d` (extend from the current expiry,
**not** from the new start's timestamp). Source sample: `1,start,M,10` then `2,start,M,4` → expiry
`11 + 4 = 15`: active through 15, inactive from 16. Rules for the corners (reconstructed, documented):
- an **unlimited** subscription is unaffected by any later `start` (with or without duration);
- a `start` **without** duration on a finite subscription makes it unlimited;
- if the user's subscription has already **expired** or was `end`ed (or never existed) the start begins a
  fresh period from its own timestamp: `new_expiry = t + d`;
- "still active at `t`" uses the same inclusive test as `check` (`t ≤ current_expiry`), so a start exactly on
  the expiry timestamp extends it.

## Worked examples
```
PART 1
1,start,Michael
5,check,Michael      -> active
7,end,Michael
8,check,Michael      -> inactive
9,check,Alice        -> inactive     (never started)
```
```
PART 2
1,start,Michael,9
10,check,Michael     -> active       (10 ≤ 1 + 9)
11,check,Michael     -> inactive     (11 > 10)
12,start,Michael
20,check,Michael     -> active       (unlimited)
21,start,Michael,2
24,check,Michael     -> inactive     (replaced by a finite one ending at 23)
```
```
PART 3
1,start,Michael,10
2,start,Michael,4
15,check,Michael     -> active       (11 + 4 = 15)
16,check,Michael     -> inactive
1,start,Alice
3,start,Alice,2
100,check,Alice      -> active       (unlimited is never shortened)
```
Same lines, different part:
```
1,start,M,10 / 2,start,M,4 / 7,check,M   -> PART 2: inactive (expiry 6)   PART 3: active (expiry 15)
```
The PART 2 example run under PART 3 prints `active inactive active active`: the unlimited start at 12 is
not shortened by `21,start,Michael,2`.

## 关联知识点

- [[s01-read-full-spec-first|S01 先读完整份规格，为 Part N+1 而设计]]
- [[s02-line-oriented-parsing|S02 面向行的解析（分隔符、类型化字段、坏行）]]
- [[s03-small-record-modeling|S03 用小记录 + 按 id 索引的字典建模]]
- [[s05-threshold-semantics|S05 阈值语义：严格 vs 非严格、计数 vs 比例、最小量门槛]]
- [[s10-event-stream-reversal|S10 事件流 + 反向事件]]
- [[s12-time-and-dates|S12 时间与日期]]
- [[s19-incremental-design-parse-model-compute-render|S19 增量式设计：parse → model → compute → render]]
