---
nodes: [problems.social.social-graph-search, distributed.partitioning.schemes]
tags: [problem]
---
# Drill: Design a social graph store with friend search, like Facebook's friend graph

Design the storage and query layer for a social graph with 100M daily active users, each
with roughly 300 direct connections, spread across billions of edges. Support looking up a
user's direct connections, finding mutual friends between two users, generating
friend-of-friend candidates, and answering "how many degrees of separation" between two
users within a bounded search depth.

**Constraints to state and honor**
- 100M DAU, ~300 friends/user (~15B undirected edges), ~500K edge writes/day (peak ≈29 QPS).
- Direct-connection reads must stay P99 < 100ms; mutual-friend reads P99 < 300ms; a
  bounded-depth shortest-path query P99 < 1s.
- A friendship is a mutual relationship materialized as two directed rows that must never
  go out of sync (one side shows the connection, the other doesn't).
- Friend-of-friend candidate generation must be paginated, never returned as one unbounded
  batch, and shortest-path queries must not search indefinitely past a bounded depth.

**Grading points**
- Partitions the edge store by hashing on user id rather than attempting community-aware
  graph partitioning, and explains why optimal graph partitioning decays over time
  ([[problems-social-graph-search-graph-partitioning-decay]]).
- Shows that a mutual-friends query only touches 2 shards regardless of how the rest of the
  graph is partitioned ([[problems-social-graph-search-mutual-friends-two-shard-cost]]).
- Chooses bidirectional BFS over single-direction BFS for shortest path and can state the
  order-of-magnitude difference in nodes explored ([[problems-social-graph-search-bidirectional-bfs-exponent-halving]]).
- Explains why an all-pairs shortest-path table is never precomputed at this scale
  ([[problems-social-graph-search-why-not-precompute-all-pairs-shortest-path]]).
- Justifies caching the entire raw graph rather than only a hot subset, and contrasts a
  graph cache miss with a precomputed feed cache miss ([[problems-social-graph-search-raw-edge-cache-vs-feed-inbox]]).
- Indexes typed edges (friend/follow/blocked) by `(edgeType, srcId)` rather than filtering
  a single index at the application layer ([[problems-social-graph-search-typed-edge-inverted-index]]).
- Picks strong cross-shard consistency for the two directions of an edge at this write
  volume, and can say when that choice would stop making sense
  ([[problems-social-graph-search-strong-consistency-tradeoff-by-write-volume]]).
- Identifies a high-degree account (a public figure/organization) as a distinct kind of hot
  spot and states a concrete mitigation ([[problems-social-graph-search-high-degree-node-hotspot]]).

**Solution**: [[solution-social-graph-search]] — attempt first, then read.

**Attempt log**
- [ ] Attempt 1 (date, 40 min, self-graded notes):
