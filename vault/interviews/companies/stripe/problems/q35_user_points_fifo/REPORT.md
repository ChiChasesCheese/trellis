# q35 User Points — report

## Summary
Ledger-style points with per-payer attribution: spend the oldest points first, never let a payer
go negative, and handle partner corrections (negative transactions). It is a tiny FIFO
ledger — the same shape as Stripe balance transactions consumed oldest-first — dressed up with
out-of-order timestamps and a subtle netting rule.

## Sources & confidence
medium-high — joeytor/StripeInterview `UserPoints.java` (README → Phone Interview) carries the
verbatim prompt, example and JUnit assertions. The same prompt is the public Fetch Rewards
take-home, so it is likely borrowed; the Stripe repo lists it as asked in a phone screen.

## Approach by part
1. `add`: append `[ts, seq, payer, points]`, keep a per-payer balance dict (first-add order).
2. `spend`: sort by `(ts, seq)`, walk positives oldest-first taking `min(remaining, need)`;
   aggregate per payer in first-consumption order; entries keep their remainder for later spends.
3. Negative transactions are netted lazily before the walk: each negative (oldest first) cancels
   its payer's oldest remaining positives via a per-payer deque. `add` rejects a negative that
   would push the payer's sum below zero, which guarantees the deque never runs dry.
4. Spend is checked against the total balance up front → atomic; `ValueError` → `ERROR` line.

## Conflicts resolved
- The repo's JUnit strings list payers in `HashMap` order; the README example lists them by
  first consumption (DANNON, UNILEVER, MILLER COORS). Primary = first consumption / first add.
- The repo's Java nets a negative at the moment it is reached in the FIFO walk (`min(-200, need)`),
  which happens to reproduce the example but breaks when the negative precedes its payer's
  positives; the netting rule above reproduces the example and stays non-negative.

## Pitfalls hidden tests target
- adds out of timestamp order (the verbatim example); negative dated before the positive it cancels
- exact-balance spend ok, +1 → error with state untouched; `SPEND,0` → empty line
- same timestamp → insertion order; per-payer aggregation across several consumed entries
- payer names with spaces; zero balances still printed

## Complexity & measured cost
O(n log n) per spend (sort of a nearly-sorted list) + O(n). Measured: 0.27s, 64 MB
(100k adds, 10 spends; budget 2 s / 256 MB).

## Test inventory
16 tests — part1: 3 · part2: 5 (incl. 1 io) · part3: 4 · part4: 4 (incl. 1 perf); edge 8 · fmt 2.

## Skills exercised
S02 parsing · S03 domain modeling · S08 deterministic ordering · S10 event streams · S12 timestamps · S17 ledger balances · S18 error paths
