---
nodes: [correctness.outbox]
url: https://microservices.io/patterns/data/transactional-outbox.html
tags: [canonical]
---
# Transactional Outbox (microservices.io, Chris Richardson)

The canonical pattern writeup for the dual-write problem: commit the event
into an outbox table in the same local transaction as the state change, then
relay it to the broker. Short, precise, with the relay variants diagrammed.

**Extract on read:**
- Why DB-write-then-publish loses events (crash between the two) and publish-then-write is worse.
- Polling publisher vs transaction-log tailing (CDC) as the relay.
- The outbox gives at-least-once publish — consumers still need idempotency.

%% trellis:begin %%
## Source
[Open the original ↗](https://microservices.io/patterns/data/transactional-outbox.html)

## Archived copy
![[microservices-io-outbox-clip]]
%% trellis:end %%
