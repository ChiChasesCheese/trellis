%% trellis:begin %%
# Payment System
*Design Problems / Commerce, Booking & Money*

Idempotent charge flows through a PSP, the ledger behind them, reconciliation and retries.

**Core** — part of the first pass through this subject.

**Requires:** [[domains/system-design/map/correctness.idempotency|Idempotency]], [[domains/system-design/map/correctness.ledger|Ledgers & Reconciliation]]

## Readings
- [[solution-payment-system|设计题解：支付系统（Payment System）]]
- [[src-square-books-payment-system|Books: an immutable double-entry accounting database service]]
- [[src-uber-batching-payment-system|Building High Throughput Payment Account Processing]]
- [[src-uber-zerosum-payment-system|Zero-Sum by Design: 10 Years of Uber's Payments Platform]]
- [[stripe-idempotency|Designing robust and predictable APIs with idempotency (Stripe)]]
- [[stripe-ledger|Ledger: Stripe's system for tracking and validating money movement]]

## Drills
- [[design-payment-ledger|Drill: Design a payment ledger service]]

## Cards (8)
1. [[problems-payment-system-ledger-entries-per-charge]]
2. [[problems-payment-system-dual-idempotency-keys]]
3. [[problems-payment-system-write-intent-before-call]]
4. [[problems-payment-system-timeout-as-unknown]]
5. [[problems-payment-system-append-only-reversing-entries]]
6. [[problems-payment-system-three-way-vs-two-way-recon]]
7. [[problems-payment-system-hot-fee-account-decouple-balance]]
8. [[problems-payment-system-10x-batching-vs-sharding]]
%% trellis:end %%

## Notes
