# q37 Fraud Rule Timestamps — report

## Summary
Replay authorization requests against a *history* of fraud rules: a rule applies only from its
effective time forward (no retroactive flagging), rule versions supersede each other, versions can
expire, and the input may be unordered. The difficulty is entirely in time boundaries and
version selection, not in expression parsing (that is q01/q12).

## Sources & confidence
medium — one phone-screen write-up (adonais0, 2021-06) giving the rule shape ("merchant of
bobs_burgers is fraudulent"), the non-retroactivity rule and the output columns. The condition
mini-language, versioning, expiry and ordering are reconstructions marked as such.

## Approach by part
1. `Version(effective_from, seq, effective_to, condition)` per rule name; `in_force` =
   `bisect_right(versions, (t, inf)) - 1` → latest version with `effective_from <= t`.
2. Same name = versions; only the in-force version is evaluated; `none` switches a rule off; any
   rule matching → `REJECT`.
3. 5-field lines carry `effective_to`; alive iff `t < effective_to` (exclusive); an expired
   selected version does not fall back to an older one (consistent with q36's TTL rule).
4. Everything is parsed first, versions sorted by `(effective_from, seq)`, requests sorted by
   `(timestamp, id)` — so line order never matters.

## Pitfalls hidden tests target
- `t == effective_from` applies, `t == effective_to` expired
- request matching an older version but not the in-force one; expired v2 must not revive v1
- `amount` compared numerically, `!=`/`<=` operators; `none` version
- output tie-break `(timestamp, id)` with `id` in string order (`a10` < `a2`)
- rules declared after requests; no rules → all `APPROVE`

## Complexity & measured cost
O((R + A) log) parse/sort + O(A · rules) evaluation. Measured: 0.52s, 72 MB
(100k requests, 50 rules × 4 versions, shuffled; budget 2 s / 256 MB).

## Test inventory
15 tests — part1: 4 · part2: 4 (incl. 1 io) · part3: 3 · part4: 4 (incl. 1 perf); edge 8 · fmt 1.

## Skills exercised
S02 parsing · S03 domain modeling · S05 strict vs non-strict comparisons · S08 deterministic sort · S10 event streams · S12 time handling · S13 inclusive/exclusive boundaries
