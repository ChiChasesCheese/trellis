%% trellis:begin %%
# Idempotency & De-duplication
*Modeling in the Small*

Repeated ids, replayed events and double frees — recognizing the second occurrence and making the handler a no-op without losing the first.

## Readings
- [[stripe-idempotency-blog|Designing robust and predictable APIs with idempotency (Stripe)]]
- [[stripe-idempotent-requests|Idempotent requests (Stripe API reference)]]

## Drills
- [[event-stream-with-reversals|Drill: an event stream with reversals, in four unlocking parts]]
- [[oa-q06-atlas-company-name|Drill: check, register, and reclaim company names by canonical form]]
- [[oa-q10-payment-intent-commands|Drill: replay PaymentIntent commands through a lifecycle state machine]]
- [[oa-q24-server-allocator|Drill: hand out the smallest free server number per host type]]
- [[oa-q25-invoice-reconciliation|Drill: match payments to invoices under relaxing rules]]
- [[oa-q27-payment-ledger|Drill: a payment ledger with three-state idempotency and partial refunds]]

## Cards (6)
1. [[cc-model-idem-dedupe-key-choice]]
2. [[cc-model-idem-double-free]]
3. [[cc-model-idem-replay-no-second-row]]
4. [[cc-model-idem-reused-id-after-close]]
5. [[cc-model-idem-same-key-different-payload]]
6. [[cc-model-idem-second-occurrence-noop]]
%% trellis:end %%

## Notes
