---
nodes: [problems.foundations.distributed-cache, caching.invalidation, distributed.partitioning.skew]
tags: [problem]
---
# Drill: Design a distributed cache (Memcached/Redis-class) in front of a database

Design a look-aside distributed cache for an application with 200M DAU: application code
checks the cache first, falls back to the database on a miss, and repopulates the cache.
The cache does not need to be durable — losing its contents is acceptable — but it must
protect the database from being overwhelmed.

**Constraints to state and honor**
- ~4,166,667 peak GET QPS, driven by a ~40x fan-out multiplier (distinct keys per page
  load), not by raw user action rate.
- Target steady-state hit rate ≥ 98%; GET P99 < 5ms.
- Cluster must add/remove nodes online; a single node or shard failure must degrade, not
  outage, the system.
- No cross-key transactions; invalidation is via DELETE, not overwriting with a new value.

**Grading points**
- Computes cache QPS from a fan-out multiplier rather than from user action rate, and
  states why this differs from sizing a durable key-value store
  ([[problems-distributed-cache-fanout-multiplier-qps]]).
- Quantifies how a hit-rate drop non-linearly multiplies backend database load (e.g. 98%
  → 90% hit rate ≈ 5x database load), and identifies this as the system's most dangerous
  failure mode ([[caching-hit-rate-outage-math]]).
- Designs the miss path with a lease-like mechanism to prevent both thundering herd and
  stale sets, rather than letting concurrent misses all query the database
  ([[problems-distributed-cache-lease-thundering-herd]]).
- Picks a sharding/routing approach (client-side, proxy, or protocol-level like Redis
  Cluster's hash slots) and can state what each makes pay for topology changes
  ([[problems-distributed-cache-sharding-tradeoffs]]).
- Explains why a single global LRU list doesn't scale under memory pressure, and how
  Memcached (slab classes) or Redis (approximate sampling) avoid it
  ([[problems-distributed-cache-eviction-slab-vs-approx-lru]], [[caching-lru-vs-lfu]]).
- Detects and mitigates a hot key by replication under suffixed copies rather than adding
  shards, which does nothing for a single overloaded key
  ([[problems-distributed-cache-hot-key-mitigation]], [[caching-hot-key-replication]]).
- Warms a cold node or cluster from an already-warm peer instead of letting it slam the
  database with a miss storm ([[problems-distributed-cache-cold-start-peer-warm]]).
- States the trade-off between an unreplicated cache (Memcached-style, cheaper memory,
  hit rate drops to zero on node failure) and a replicated one (Redis Cluster-style,
  double memory, hit rate preserved on failover)
  ([[problems-distributed-cache-durability-tradeoff-memcached-vs-redis]]).

**Solution**: [[solution-distributed-cache]] — attempt first, then read.

**Attempt log**
- [ ] Attempt 1 (date, 40 min, self-graded notes):
