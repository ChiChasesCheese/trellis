---
nodes: [round.reading, chrono.intervals, transfer.stripe-oa]
tags: [stripe-oa, q11]
---
# Drill: a subscription database whose renewal rule flips itself

Sixty minutes, stdin to stdout. Events arrive one per line, `timestamp,op,user[,duration]`,
processed strictly in the order given — not resorted — describing a per-user Stripe Billing
subscription: `start` (optionally for a fixed duration), `end` (cancel), and `check` (report
active/inactive). Part 1 has unlimited subscriptions only. Part 2 adds fixed durations,
inclusive of the boundary, where a new `start` replaces whatever the user already had. Part 3
keeps the same input shape but reverses that rule: a `start` that lands while the user is still
active extends the current expiry instead of overwriting it.

**Constraints to state and honor**
- First line `PART n` (1..3); `timestamp,op,user[,duration]` with duration only on `start`
  (Parts 2–3); user names case-sensitive; up to 2·10^5 lines.
- Output one line per `check` event in input order: `active` or `inactive`; `start`/`end` print
  nothing.
- The active test is inclusive: `c ≤ t + d`; `d = 0` is active only at `t` itself.
- Same-timestamp events apply in input order, not re-sorted, even if timestamps go backwards.

**Grading points**
- Read Part 3 before writing Part 2's expiry-overwrite logic — the two are opposite rules on the
  same field, and a single `simulate(events, mode)` with a mode switch is the shape that survives
  both.
- Per-user state is one value: `None` for unlimited, an integer expiry, or absent for
  never-subscribed/ended.
- Part 3's extension is measured from the user's *current* expiry, not from the new start's own
  timestamp — the two give different answers and only one matches the worked example.
- The four corner rules for Part 3 stated out loud: unlimited is never shortened, a no-duration
  start on a finite subscription upgrades it to unlimited, an expired or ended subscription
  restarts fresh from the new timestamp, and "still active" uses the same inclusive test as
  `check`.
- `end` on an unknown or already-ended user is a no-op, never an error.

**Source**
- `vault/interviews/companies/stripe/problems/q11_subscription_database/problem.md`, `vault/interviews/companies/stripe/problems/q11_subscription_database/REPORT.md`, `vault/interviews/companies/stripe/problems/q11_subscription_database/problem.md`, `vault/interviews/companies/stripe/study/10-solutions/q11_subscription_database.md`, `vault/interviews/companies/stripe/study/10-solutions/q11_subscription_database.md`

**Attempt log**
- [ ] Attempt 1 (date, 60 min, self-graded notes):
