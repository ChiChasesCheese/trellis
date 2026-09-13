# qA05 · LC 1604 Alert Using Same Key-Card ≥3 Times in 1 Hour — HH:MM, per-name sort, window of 3, (k, window), rate limiter

**Type:** LeetCode "Stripe" tag (algorithm) · **Stage:** phone screen / OA part 1 · **Last asked:** tag snapshot 2026-07-12 (all-time bucket)
**Frequency:** tag freq 61.2 (liquidslr All 2025-06), 62.5 (snehasishroy all 2026-07); absent from the >6-month files, so it is a relatively recent addition · 2 tag mirrors · **Confidence:** medium-high

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

## Edge cases hidden tests are known to target
- window inclusive: exactly 60 minutes alerts; 61 does not; no midnight wrap (`23:30` then `00:10` is 20 min *back*, not 40 forward)
- duplicate identical times (`10:40, 10:40`) count as separate uses
- unsorted input per name; a name with < 3 uses can never alert; result must be unique + sorted
- `HH:MM` zero-padded parsing (`09:05`); output names sorted as plain strings
- Part 3: denied swipes do not count; boundary `t - window` inside the window; out-of-order → error

## Variants seen in the wild
- q23 rate limiter (5 requests / 2 s per client; sliding window, weighted requests, token bucket).
- qA04 invalid transactions (window over *different-city* pairs instead of counts).
- Return the first alert time per name instead of the name list.

## Why Stripe asks it
Radar card-testing detection and API rate limiting are the same shape: per-key sorted timestamps and a
fixed-width window; the inclusive boundary and the "denied requests don't count" rule are the traps.

## Stripe-flavored follow-ups
1. Parametrize `(k, window)` and reuse the same scan — Part 2.
2. Turn the audit into a limiter that blocks the k-th use online — Part 3 (q23).
3. Return which swipes were part of the offending window (see qA04 Part 2 reasons).

## What this tests
skills: A07 window over sorted timestamps · S02 parsing · S04 grouping · S05 threshold semantics · S12 time parsing · S16 sliding window

## Sources
- https://leetcode.com/problems/alert-using-same-key-card-three-or-more-times-in-a-one-hour-period
- https://raw.githubusercontent.com/liquidslr/leetcode-company-wise-problems/main/Stripe/5.%20All.csv (61.2)
- https://raw.githubusercontent.com/snehasishroy/leetcode-companywise-interview-questions/master/stripe/all.csv (62.5)
- catalog/raw/github_repos.md §30
