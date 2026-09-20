---
nodes: [problems.geo.ride-hailing, distributed.consistency, networking.realtime]
tags: [problem]
---
# Drill: Design a ride-hailing backend like Uber

Design the backend for a ride-hailing service: drivers continuously report their location,
riders request a ride and get matched to a nearby driver, and the trip progresses through a
state machine from request to completion. Surge pricing adjusts fares by region during
supply/demand imbalances.

**Constraints to state and honor**
- Roughly 40 million trips/day (peak ride-request QPS in the low thousands) against roughly
  9.7 million monthly drivers, a small fraction of whom are online concurrently at peak.
- Drivers report location on the order of every few seconds; matching must complete in
  single-digit seconds P99.
- The same driver must never be bound to two trips at once, even under concurrent match
  attempts for the same area.
- Both rider and driver clients need near-real-time, bidirectional-capable updates without
  polling on every state change.

**Grading points**
- States why driver location ingestion runs on a pipeline entirely separate from the trip
  database, quantifying why it is roughly two orders of magnitude higher throughput than
  matching requests ([[problems-ride-hailing-ingestion-vs-matching-order-of-magnitude]]).
- Uses an explicit short-TTL exclusive lock on a candidate driver before sending a match
  invitation, and explains why optimistic concurrency is the wrong tool here
  ([[problems-ride-hailing-exclusive-lock-not-optimistic]]).
- Chooses a bidirectional real-time transport (WebSocket) over SSE for this specific case and
  explains why the driver side's need to send data back rules out a one-directional channel
  ([[problems-ride-hailing-websocket-bidirectional]], [[networking-realtime-transport-choice]]).
- Designs surge pricing as a separate streaming aggregation pipeline with a cached
  region-to-multiplier lookup, not a per-request computation
  ([[problems-ride-hailing-surge-streaming-precompute]]).
- Explains why a hexagonal grid avoids a directional bias that a rectangular grid would
  introduce into a supply/demand gradient computation
  ([[problems-ride-hailing-hexagon-supply-demand-gradient]]).
- States that a distributed-lock-store outage has no safe degraded mode for match
  exclusivity — matching requests must queue, not fall back to unlocked matching
  ([[problems-ride-hailing-lock-outage-no-safe-fallback]]).
- Recognizes that different parts of the system carry different consistency promises — match
  exclusivity needs strong guarantees while most state-machine updates can be eventually
  consistent — rather than picking one consistency level for the whole design
  ([[distributed-consistency-ladder]]).
- Describes how ingestion and matching must share the same hierarchical spatial cell as their
  shard key at 10x scale, so a typical matching query stays within one shard
  ([[problems-ride-hailing-10x-shared-shard-key]]).

**Solution**: [[solution-ride-hailing]] — attempt first, then read.

**Attempt log**
- [ ] Attempt 1 (date, 40 min, self-graded notes):
