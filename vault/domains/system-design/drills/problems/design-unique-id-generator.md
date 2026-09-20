---
nodes: [problems.foundations.unique-id-generator, distributed.time.clocks]
tags: [problem]
---
# Drill: Design a unique ID generator

Design a service that hands out unique, roughly time-ordered 64-bit IDs used as primary
keys across many internal systems (posts, orders, events). Generation logic will be
embedded into thousands of independent deployment units, not run as a small dedicated
fleet, and must never depend on a network call on the hot path.

**Constraints to state and honor**
- ~5,000 independent generator identities (e.g. one per database shard); platform-wide
  average 20,000 IDs/s, peak 200,000 IDs/s.
- P99 generation latency < 1ms — no network I/O allowed in `GenerateId()` itself.
- IDs must be strictly increasing per generator node; cross-node ordering only needs to be
  approximate (bounded by clock skew).
- The system's clock coordination service can go down without stopping already-running
  generator nodes from producing IDs.

**Grading points**
- Allocates the 64-bit budget across timestamp, worker-id, and sequence based on how many
  independent generator identities the deployment needs, not by copying a well-known
  system's split verbatim ([[problems-unique-id-generator-worker-id-bits-from-deployment-count]]).
- Recognizes that sequence-bit capacity is not the real bottleneck at this scale and argues
  the number instead of assuming a bigger sequence field is always safer
  ([[problems-unique-id-generator-sequence-bits-not-bottleneck]]).
- Embeds generation as a local, in-process (or data-layer) call instead of a separate
  network service, and explains why the latter reintroduces the dependency the design
  exists to avoid ([[problems-unique-id-generator-embedded-vs-service-placement]]).
- Detects a local clock rollback and refuses to generate rather than silently reusing an
  earlier timestamp ([[problems-unique-id-generator-clock-rollback-refuse]], [[distributed-clock-error-sources]]).
- Distinguishes sequence exhaustion (a sub-millisecond, self-resolving stall) from worker-id
  exhaustion (a deployment-scale problem needing lease reclamation and eventually a bit-width
  migration) ([[problems-unique-id-generator-two-exhaustion-scales]]).
- States that already-running nodes keep generating IDs when the lease coordinator is down,
  and only new-node startup and renewal are affected ([[problems-unique-id-generator-lease-coordinator-outage]]).
- Knows the trade-off against UUIDv7 as the nearest coordination-free alternative, including
  why pure randomness doesn't collide at this scale ([[problems-unique-id-generator-uuidv7-collision-math]]).
- Uses a monotonic clock (not wall clock) to detect elapsed-time anomalies ([[distributed-monotonic-vs-wallclock]]).

**Solution**: [[solution-unique-id-generator]] — attempt first, then read.

**Attempt log**
- [ ] Attempt 1 (date, 40 min, self-graded notes):
