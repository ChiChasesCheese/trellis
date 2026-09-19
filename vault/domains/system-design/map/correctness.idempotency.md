%% trellis:begin %%
# Idempotency
*Correctness Patterns*

Idempotency keys, dedup windows, and designing every mutation to survive a retry.

**Core** — part of the first pass through this subject.

**Requires:** [[domains/system-design/map/async.delivery|Delivery Semantics]]

**Unlocks:** [[domains/system-design/map/correctness.ledger|Ledgers & Reconciliation]]

## Readings
- [[stripe-idempotency|Designing robust and predictable APIs with idempotency (Stripe)]]

## Cases
- [[qs-content-addressed-intake-with-recorded-rejections|Content-addressed intake, with rejections on the record]] — `quant-stroller`
- [[qs-resumable-ingestion-against-a-metered-api|Resumable ingestion against a metered API]] — `quant-stroller`

## Drills
- [[design-payment-ledger|Drill: Design a payment ledger service]]

## Cards (7)
1. [[correctness-idempotency-key-design]]
2. [[correctness-idempotency-payload-hash]]
3. [[correctness-idempotency-response-replay]]
4. [[correctness-idempotency-concurrent-retries]]
5. [[correctness-idempotency-partial-failure]]
6. [[correctness-dedup-window]]
7. [[correctness-idempotent-consumer-patterns]]
%% trellis:end %%

## Notes
