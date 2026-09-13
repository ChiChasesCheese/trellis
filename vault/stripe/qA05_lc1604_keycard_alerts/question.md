# qA05 · LC 1604 Alert Using Same Key-Card ≥3 Times in 1 Hour — HH:MM, per-name sort, window of 3, (k, window), rate limiter

LC 1604 · *Alert Using Same Key-Card Three or More Times in a One Hour Period* · Medium · https://leetcode.com/problems/alert-using-same-key-card-three-or-more-times-in-a-one-hour-period

## The problem (restated)
Two parallel lists: `key_name[i]` used a key-card at `key_time[i]` (`"HH:MM"`, 24-hour, all on the same
day). A worker gets an **alert** when they use their card **three or more times within any one-hour
period, inclusive** — `10:00, 10:40, 11:00` triggers, `22:51, 23:52` does not (61 minutes; and the day
does not wrap). Return the alerted names, **unique, sorted ascending**. Input is not sorted.
LC limits: `1 ≤ n ≤ 10^5`, names are 1–10 lowercase letters, valid times.

## Context
This is q23's rate limiter seen from the audit side: "≥ k events per key inside a trailing window"
is Radar's card-testing rule (many attempts on one card in minutes), Stripe's API-abuse alerting, and
the 5-requests-per-2-seconds phone-screen limiter. Parsing `HH:MM`, grouping by key, sorting, and a
fixed-size window over sorted timestamps is the whole exercise; the follow-ups generalize `(k, window)`
and flip the batch alert into an online limiter that *denies* the k-th swipe.

## Input (stdin)
```
PART n                 # 1..3
k window               # Part 2: integers (window in minutes); Part 3: limit window
name HH:MM             # one swipe per line (any order for Parts 1–2; chronological per name for Part 3)
...
```

## Output
* Parts 1–2: alerted names, one per line, sorted; nothing when none.
* Part 3: one line per swipe in input order: `name HH:MM ALLOW` or `name HH:MM DENY`.

## Rules
### Part 1 — LC signature  `alert_names(key_name, key_time) -> list[str]`
Convert `HH:MM` to minutes since midnight. Group times by name, sort each list, and alert the name if
for some `i`, `times[i+2] - times[i] ≤ 60`. Return `sorted(set(alerted))`.

### Part 2 — generic threshold  `alert_names_k(key_name, key_time, k=3, window=60) -> list[str]`
Alert iff some `i` has `times[i+k-1] - times[i] ≤ window`. `k = 1` alerts every name that appears at
all (a single swipe is "1 use within any window"); `k ≤ 0` or `window < 0` → `ValueError`.
`alert_names == alert_names_k(k=3, window=60)`.

### Part 3 — per-key limiter  `KeyCardLimiter(limit=2, window=60).swipe(name, time) -> bool`
Online: `swipe` returns `True` (allowed) iff **fewer than `limit` allowed swipes** of that name lie in
`[t - window, t]` (inclusive). Denied swipes **do not count** toward later windows (q23 rule). Swipes
per name must be in non-decreasing time; a step backwards raises `ValueError`. `limit=2, window=60`
is the limiter that denies exactly the swipe that would have caused LC's alert.
`denied` lists `(name, time)` of the denied swipes in order.

## Worked examples
```
LC ex1  names=[daniel,daniel,daniel,luis,luis,luis,luis] times=[10:00,10:40,10:40,09:40,11:00,13:00,15:00]
        daniel 10:00,10:40,10:40 (40 min) -> alert; luis 09:40,11:00,13:00,15:00 -> no      -> ["daniel"]
LC ex2  names=[alice,alice,alice,bob,bob,bob,bob] times=[12:01,12:00,18:00,21:00,21:20,21:30,23:00]
        alice sorted 12:00,12:01,18:00 -> 6 h -> no ; bob 21:00,21:20,21:30 -> 30 min -> yes     -> ["bob"]
Bound   ["a","a","a"] ["10:00","10:40","11:00"] -> ["a"] (exactly 60) ; ["10:00","10:40","11:01"] -> []
Part 2  ex2 with k=2, window=1  -> ["alice"] (12:00 & 12:01) ; k=4, window=120 -> ["bob"] (21:00..23:00 = 120)
        k=1 -> ["alice","bob"]
Part 3  limit=2, window=60: a 10:00 ALLOW, a 10:40 ALLOW, a 11:00 DENY (2 allowed in [10:00,11:00]),
        a 11:01 ALLOW (10:00 left the window; 10:40 counts, the denied 11:00 does not), a 11:40 DENY
```
stdin Part 1 ex2 → `bob`.

## 关联知识点

- [[a07-per-key-sliding-window|A07 每 key 上按时间排序的滑动窗口]]
- [[s02-line-oriented-parsing|S02 面向行的解析（分隔符、类型化字段、坏行）]]
- [[s04-group-then-aggregate|S04 分组聚合，规则每组一次而不是每行一次]]
- [[s05-threshold-semantics|S05 阈值语义：严格 vs 非严格、计数 vs 比例、最小量门槛]]
- [[s12-time-and-dates|S12 时间与日期]]
- [[s16-sliding-window-token-bucket|S16 滑动窗口计数器 / 令牌桶]]
