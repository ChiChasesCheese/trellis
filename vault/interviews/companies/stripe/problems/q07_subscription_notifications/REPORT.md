# q07 Subscription Notification Scheduler — report

## Summary
Lifecycle emails for subscriptions (welcome / expiry warning / expired) on an integer day
axis, then plan changes and renewals that rewrite the still-pending part of each user's
schedule. It is Stripe Billing's notification pipeline reduced to a small state machine per
subscription plus one deterministic global sort. The difficulty is entirely in the "already
sent vs pending" split, the same-day tie-break order, and exact tag formatting. Part 4 is the
prachub single-day rule-driven variant (`schedule_by_rules`).

## Sources & confidence
medium-high — 6 independent mentions: extrabrain 2026-02-10 (OA, 3 parts), linkjob 2025-09-16
(OA, 3 parts), linkjob 2025-12-07 (intern VO mention), oavoservice 2025-12-27, 1point3acres 题库
「Email Subscription」+ 1100699 intern VO, prachub 「Generate Account Email Notifications」
(rule-driven variant); collegesidekick repost of 1point3acres 793600.
- https://extrabrain.app/interview-questions/stripe-hackerrank-online-assessment-extrabrain/
- https://www.linkjob.ai/interview-questions/stripe-hackerrank-online-assessment/
- https://www.linkjob.ai/interview-questions/stripe-interview-questions/

## Approach by part
1. `end = start + duration`; schedule = `(start, "Welcome to <plan>")`, `(end-15, "Upcoming
   expiry")`, `(end, "Subscription expired")`; an email dated `< start` is dropped (15-day
   term: warning on the start day after the welcome; 14-day: no warning).
2. `CHANGE` takes effect at the start of its day: emails dated `< day` are locked as sent
   (with the plan name they were sent under); pending ones are recomputed with the new plan.
3. `RENEW` extends from the **old** end (`new_end = old_end + extra`), then the same
   lock-and-recompute step: an email is pending iff `day >= start and day >= since`, where
   `since` is the day of the last event. Events sorted by `(day, input index)`.
   Output tuples `(day, user_idx, 0=event/1=email, seq, payload)` are sorted with no `key=`
   and rendered afterwards — email text is formatted only at render time.
4. Index accounts by `created_day` and `expires_day`; each rule looks up one bucket
   (`current - offset`, `current + offset`, `current - offset`); `(account_idx, rule_idx)` sort.

## Pitfalls hidden tests target
- warning before the start day (dropped) vs on the start day (kept, after the welcome);
  duration 0 → welcome and expired on the same day
- tie order on one day: user input order → events before emails → schedule order
- `CHANGE` on the start day → welcome names the new plan; after the start → only `[Changed]`
- renewal on the warning day replaces the warning; one day later the warning stays and a second
  one is sent; renewal on the end day suppresses "expired"; after expiry the old one stays
- `extra_days = 0` still prints `[Renewed] 30 -> 30`; unknown users ignored; events out of
  input order are applied in day order (so the day-15 warning sits between a day-5 and a
  day-20 `[Changed]`)
- Part 4 templates keep their own commas (`split(",", 4)`); unknown trigger → `ValueError`
- memory on 10^5 users + 10^5 events: keeping the parsed event rows, per-email formatted
  strings and a `key=` sort blew the 256 MB budget (282 MB); storing only raw event lines,
  `__slots__`, lazy formatting, keyless sort and streaming output brought it to ~197 MB

## Complexity & measured cost
Parts 1–3: O((U + E) log(U + E)) for the two sorts, O(1) state per user.
Part 4: O(A + R + output). 100k users + 100k events (Part 3): ~0.95 s, ~197 MB RSS;
100k accounts + 100k rules (Part 4): ~0.24 s, ~132 MB RSS (budget 2 s / 256 MB each).
Note: `run_script` reports `RUSAGE_CHILDREN.ru_maxrss`, which is the max over *all* children
so far — the Part 4 perf test inherits the Part 3 peak when both run in one session.
Measured: 0.95s, 197 MB (Part 3 perf) · 0.24s, 132 MB (Part 4 perf)

## Test inventory
23 tests — part1: 7 · part2: 5 · part3: 7 · part4: 4; edge 10 · fmt 2 · perf 2 · io 2.
`IMPL=starter`: 21 fail / 2 pass (the whitespace-equivalence test and the Part 4 perf test are
satisfied by an empty stub; every content test fails).

## Skills exercised
S01 long spec · S02 mixed record parsing · S03 records keyed by id · S08 multi-key sort ·
S09 exact formatting with tags · S10 events that rewrite earlier decisions · S12 day arithmetic ·
S19 incremental design
