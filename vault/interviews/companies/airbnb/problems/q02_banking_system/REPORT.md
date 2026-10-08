# REPORT · q02 Banking System

## Summary

A CodeSignal ICF 4-level project, same template as q01. Level 1 is verbatim from photos; Levels 2–4 follow the
verbatim one-line summaries, with methods and semantics reconstructed from GitHub versions of the problem. Like q01 it
tests state modelling under changing requirements; the new parts are a **deferred operation with expiry** (L3) and
**point-in-time history** (L4).

## Sources & confidence

| Part | Confidence | Source |
|---|---|---|
| Format (10 tests in L1, `@timeout(0.4)`, Python unittest, sandbox rules) | high | photos → `../../catalog/raw/codesignal_banking_system_photos.md` |
| Level 1 spec, interface, example, test cases 01–03 (03 cut off after 4 lines) | high | photos, verbatim |
| Level 2–4 one-line summaries | high | photos, verbatim |
| L2 `top_activity`, L3 `transfer`/`accept_transfer` + 24 h expiry, L4 `merge_accounts`/`get_balance` | medium | FazeelUsmani/Industry-Problems (titles match the photos one-to-one) |
| L3 24 h boundary (inclusive: acceptable at `t + 86400000`) + real cases 02–04 | high | photos of the real `level_3_tests.py`, 2026-10-08 |
| Status method in L3, what "histories" means after a merge | low | sources disagree or are silent; each choice is labelled in `problem.md` |
| Company = Airbnb | low–medium | Chi; the photos name no company |

## Approach by level

1. `balances: dict[account_id, int]`, three methods.
2. A second dict `activity`, updated only on success; `sorted(key=(-total, id))[:n]`, format `id(total)`.
3. `pending: dict[transfer_id, (source, target, amount, expires_at)]`; `_expire(ts)` refunds every transfer with
   `ts > expires_at` (still acceptable at exactly `t + 1 day`), and **every** public method calls it first (lazy expiry).
4. All balance writes go through `_set_balance`, which appends `(ts, balance)` to `history[id]`; a merge appends
   `(ts, None)` to the merged id. `get_balance` = `bisect_right` on the timestamps, then `None` if the entry is `None`
   or there is none. Refunds are dated at `expires_at + 1`, not at the query that noticed them.

## Pitfalls the tests target (all verified by mutation, see below)

Re-creating an account resets it · overdraft allowed · ties not alphabetical · totals sorted as strings · failed
payment counted as activity · expiring one ms early (`<` instead of `<=`) · expiry processed only in `accept_transfer` · activity counted at
transfer time instead of on accept · transfer ordinal consumed by a failed transfer · accept by a non-target · merge
keeps the merged account's outgoing transfers · merge drops instead of redirecting incoming transfers · transfers
between the two merged accounts not cancelled · refund dated at the query time · `get_balance` exclusive of `time_at` ·
merged id still has a balance after the merge.

## Complexity + measured

create/deposit/pay/accept O(P) where P = pending transfers (the lazy scan); top_activity O(A log A); merge O(P);
get_balance O(log H). The early-exit expiry scan (creation order = expiry order, since every transfer lives 24 h) is
not needed: the plain full scan runs Level 3 in 0.08 s with 1000 pending transfers. All three perf tests together:
0.05 s on Python 3.13 (each asserts < 0.4 s). `bisect_right(..., key=...)` needs Python ≥ 3.10.

## Test inventory

42 tests: L1 10 (01–03 from the photos, 04 the statement example, 05–10 ours); L2 8; L3 13 (02r–04r copied from the real file); L4 11 (01 of L2–L4 is the
GitHub statement example, the rest ours).

- `solution_levelN.py` passes Levels 1..N and fails Level N+1 (checked for N = 1..4); `solution.py` 42/42.
- Empty `starter.py`: fails on every level (L1 10, L2 7, L3 12, L4 10).
- `python3 mutation_check.py`: 16/16 mutants killed.

## Skills exercised

Choosing the container from the four summaries · a single write path (`_set_balance`) so history cannot miss a change
· lazy expiry at the top of every method · read the boundary off the real tests, not off convention (here the 24 h window is closed) · append-only history + binary search for
"as of time t" queries · an id's lifetime as a sequence of `(ts, value | None)` events.
