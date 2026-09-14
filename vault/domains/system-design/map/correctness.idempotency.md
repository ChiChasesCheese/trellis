%% trellis:begin %%
# Idempotency
*Correctness Patterns*

Idempotency keys, dedup windows, and designing every mutation to survive a retry.

**Requires:** [[async.delivery|Delivery Semantics]]

**Unlocks:** [[correctness.ledger|Ledgers & Reconciliation]]

## Readings
- [[stripe-idempotency|Designing robust and predictable APIs with idempotency (Stripe)]]

## Cases
- [[qs-content-addressed-intake-with-recorded-rejections|Content-addressed intake, with rejections on the record]] — `quant-stroller`
- [[qs-resumable-ingestion-against-a-metered-api|Resumable ingestion against a metered API]] — `quant-stroller`

## Drills
- [[design-payment-ledger|Drill: Design a payment ledger service]]

## Cards (7)
- [[correctness-dedup-window]]
- [[correctness-idempotency-concurrent-retries]]
- [[correctness-idempotency-key-design]]
- [[correctness-idempotency-partial-failure]]
- [[correctness-idempotency-payload-hash]]
- [[correctness-idempotency-response-replay]]
- [[correctness-idempotent-consumer-patterns]]
%% trellis:end %%

## Notes
