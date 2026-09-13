# q18 Six Degrees of Collusion — report

## Summary
Fraud-ring detection from shared identifiers: customers sharing a device / card are linked,
links are transitive, and Stripe wants the suspect's direct links, its ring size (block if
≥ K), and a per-ring risk score. It is Radar's "linked accounts" heuristic reduced to
connected components. The graded difficulty is bookkeeping: same-position identifiers only,
target excluded from its own list, ring size counts the target, zero-risk members dropped
before averaging, deterministic ordering.

## Sources & confidence
high (Parts 1–3) — LeetCode 8385570 verbatim Q1–Q3 with expected outputs (2026-07-09),
1point3acres 题库 titles "Direct Links / Fraud Ring Size / Risk Scoring" (last asked 2026-06-24),
InterviewDB "Collusion — OA". medium (Part 4) — linkjob phone screen weights
(name .2 / email .5 / company .3, threshold .5) and csoahelp VO weighted-score part.
Conflict resolved: the post's Q2 record `E:d2:123` contradicts its own expected answer
(largest = 3); the commenter's typo reading is adopted (E's card made distinct).

## Approach by part
1. `direct_links`: map `(position, value) → customers`; union over the target's records; drop
   target; sort.
2. `groups`: union-find keyed by customer, unioning every owner list of each identifier;
   components emitted in first-appearance order. `ring_size` (includes target, 0 if unknown),
   `largest_ring`, `should_block = size ≥ K`.
3. `ring_risks`: risk = last record's value per customer; per ring, mean over members with
   risk ≠ 0, `0` if none remain; printed `members-sorted risk` with two decimals.
4. `weighted_links`: `user_id,name,email,company`; weights compared in integer thousandths so
   `0.2 + 0.3 ≥ 0.5` holds; case-insensitive; empty fields never match.

## Pitfalls hidden tests target
- listing the target in its own direct links; listing a pair twice when linked by 2 identifiers
- counting only one hop for "ring" (must be transitive) or excluding the target from ring size
- `K` boundary is non-strict; lone customer has ring size 1
- averaging before removing zero-risk members; all-zero ring must not divide by zero
- float threshold drift (`0.2 + 0.3 == 0.5` is False in floats)
- values at different positions treated as the same identifier

## Complexity & measured cost
O(N α(N) + C log C) for N records, C customers. Measured: 0.59s, 128 MB (100k records,
50k customers, Part 3; budget 2 s / 256 MB).

## Test inventory
22 tests — part1: 6 (incl. 1 io) · part2: 8 (incl. 1 io, 1 perf) · part3: 5 (incl. 1 io) · part4: 3;
edge 10 · fmt 2.

## Skills exercised
S02 parsing · S03 records keyed by id · S04 grouping · S05 threshold semantics · S08 deterministic order · S18 validation · S19 incremental · A16 union-find
