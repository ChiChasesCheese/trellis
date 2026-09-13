# q11 Subscription Database — report

## Summary
A per-customer subscription record driven by an ordered event stream (`start`/`end`/`check`) whose
semantics tighten part by part: unlimited → fixed duration that *replaces* → renewal that *accumulates*.
It is the "renewal extends the end date" rule from Stripe Billing reduced to one integer per user, and it
tests whether the candidate reads Part 3 before hard-coding Part 2's overwrite.

## Sources & confidence
high (rules and three sample inputs verbatim) — single source: csoahelp 2024-11-27 「Stripe – Stack Position
OA」; vocabulary corroborated by the q07 subscription-notification family (extrabrain / linkjob).

## Approach by part
1. `subs[user]` present ⇒ active; `end` pops; `check` looks up. Output only for checks, input order.
2. `subs[user] = t + d` (or `None` for unlimited); active iff `c <= expiry` (**inclusive**: `1,start,M,9` →
   active at 10, inactive at 11). Every start overwrites.
3. If the user is still active at the start's timestamp (same inclusive test) and finite:
   `expiry += d` (from the *current* expiry, not from `t`); unlimited stays unlimited; a no-duration
   start upgrades to unlimited; expired/ended users restart fresh at `t + d`.
   One `simulate(lines, mode)` with mode ∈ {basic, replace, accumulate}.

## Pitfalls hidden tests target
- off-by-one at `start + d` (inclusive) · `d = 0` active only at `t` · check before any start
- Part 3 extension measured from the new start instead of the current expiry (gives 6 instead of 15)
- extending an already-expired subscription instead of restarting it
- unlimited shortened by a later finite start (Part 3 must not; Part 2 must)
- `end` on unknown user / double `end` must not crash · same-timestamp ordering follows input order
- re-sorting events by timestamp (the spec processes them as given)

## Complexity & measured cost
O(n) time, O(users) memory. Measured: 0.16s, 44 MB (200k events, 20k users; budget 2 s / 256 MB).

## Test inventory
24 tests — part1: 9 · part2: 7 · part3: 8; edge 14 · fmt 1 · io 2 · perf 1.

## Skills exercised
S01 read the full spec · S02 optional-field parsing · S03 per-user state · S05 inclusive boundary ·
S10 ordered events with cancellation · S12 duration arithmetic · S19 incremental design
