%% trellis:begin %%
# Dual Writes & Outbox
*Correctness Patterns*

Why writing DB-then-publish loses events, and how the transactional outbox closes the gap.

**Requires:** [[domains/system-design/map/distributed.transactions|Transactions]], [[domains/system-design/map/async.queues|Message Queues]]

## Readings
- [[microservices-io-outbox|Transactional Outbox (microservices.io, Chris Richardson)]]

## Cards (6)
1. [[correctness-dual-write-problem]]
2. [[correctness-outbox-mechanism]]
3. [[correctness-outbox-event-payload]]
4. [[correctness-outbox-ordering-cloze]]
5. [[correctness-outbox-relay-lag]]
6. [[correctness-outbox-cleanup]]
%% trellis:end %%

## Notes
