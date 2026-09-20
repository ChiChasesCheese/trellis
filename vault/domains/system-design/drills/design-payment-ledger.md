---
nodes: [correctness.ledger, correctness.idempotency, distributed.transactions, async.log, problems.commerce.payment-system]
tags: [fintech, flagship]
---
# Drill: Design a payment ledger service

Design the ledger at the core of a payment platform: it records every money
movement (charges, refunds, payouts, fees), serves balance queries, and feeds
settlement and reconciliation.

**Constraints to state and honor**
- 5k writes/s peak, entries immutable, zero tolerance for lost or double-counted money.
- Balance reads: merchant dashboard (stale OK) vs payout eligibility check (must be exact).
- One merchant (hot account) can be 10% of total volume.
- Daily settlement cutoff; external reconciliation against processor files.

**Grading points (what a strong answer hits)**
- Double-entry invariant enforced at write time; corrections as reversing entries ([[correctness-double-entry-invariant]], [[correctness-ledger-immutability]]).
- Idempotency keys on the write API; stored-response replay ([[correctness-idempotency-response-replay]]).
- Balance = snapshot + delta replay; hot-account strategy ([[correctness-ledger-hot-accounts]], [[correctness-balance-derivation]]).
- Ledger as append-only log feeding derived views ([[analytics-derived-data-framing]]).
- Cutoff semantics and three-way reconciliation ([[correctness-ledger-cutoff-settlement]], [[correctness-ledger-three-way-recon]], [[problems-payment-system-three-way-vs-two-way-recon]]).
- Isolation level choice for concurrent entry + balance check ([[distributed-write-skew]]).
- PSP-side idempotency key layered on top of the client-facing one, so losing our own state never causes a second real charge ([[problems-payment-system-dual-idempotency-keys]]).
- A PSP call timeout is treated as unknown, never retried blindly — the pending ledger entry is written before the call so recovery can query the PSP's true state instead of guessing ([[problems-payment-system-timeout-as-unknown]], [[problems-payment-system-write-intent-before-call]]).
- The platform fee account is touched by every charge, so its write rate tracks total system throughput regardless of merchant-based sharding; at 10x volume this forces batched writes rather than further sharding ([[problems-payment-system-hot-fee-account-decouple-balance]], [[problems-payment-system-10x-batching-vs-sharding]]).

**Solution**: [[solution-payment-system]] — attempt first, then read.

**Attempt log**
- [ ] Attempt 1 (date, 40 min, self-graded notes):
