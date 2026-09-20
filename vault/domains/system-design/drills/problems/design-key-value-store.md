---
nodes: [problems.foundations.key-value-store, distributed.replication.leaderless, distributed.partitioning.schemes]
tags: [problem]
---
# Drill: Design a highly-available distributed key-value store

Design a Dynamo-style key-value store: `get(key)` / `put(key, value)` / `delete(key)`
only, backing session, shopping-cart and preference data for a platform with 300M monthly
active users. Writes must keep succeeding even when a minority of nodes are unreachable.

**Constraints to state and honor**
- ~555,556 peak client QPS (read:write ≈ 9:1), ~3.6 TB of data at N=3 replication.
- 99.9% of reads and writes complete within 300ms at peak load (align with Dynamo's
  published SLA).
- Eventual consistency: concurrent writes must never be silently dropped.
- The cluster must add/remove physical nodes online without a full remap of the key space.

**Grading points**
- Sizes the cluster by per-node operation throughput under N-way replication fan-out
  (QPS × N), not by raw byte count, and explains why storage capacity is not the binding
  constraint here ([[problems-key-value-store-qps-bound-not-storage-bound]]).
- Chooses consistent hashing with virtual nodes over range partitioning or a fixed
  `hash(key) % P` scheme, and explains why the alternatives make online rebalancing
  expensive ([[problems-key-value-store-consistent-hashing-vnode-choice]], [[distributed-consistent-hashing]]).
- Picks an N/R/W quorum configuration (e.g. N=3, R=2, W=2) satisfying W+R>N, and can
  compute how quorum reads/writes improve availability over a single node
  ([[problems-key-value-store-quorum-availability-math]], [[distributed-quorum-math]]).
- Handles a preferred node's unavailability with sloppy quorum and hinted handoff instead
  of rejecting the write, and explains why a strict quorum would violate the availability
  requirement ([[problems-key-value-store-sloppy-quorum-hinted-handoff]], [[distributed-sloppy-quorum-handoff]]).
- Resolves concurrent writes with vector clocks (returning sibling versions to the client)
  rather than last-write-wins by timestamp, and can state why LWW silently loses data
  ([[problems-key-value-store-vector-clock-vs-lww]], [[distributed-lww-danger]]).
- Uses Merkle trees for background anti-entropy repair between replicas and explains why
  this beats a full data comparison when divergence is small
  ([[problems-key-value-store-merkle-tree-anti-entropy]], [[distributed-anti-entropy-cost]]).
- Manages cluster membership with a gossip protocol rather than a centralized coordination
  service, and can reason about why convergence time scales well with cluster size
  ([[problems-key-value-store-gossip-convergence-log-n]]).
- Describes what changes mechanically at 10x scale (node count, virtual node count) and
  what stays architecturally the same (ring routing, gossip)
  ([[problems-key-value-store-10x-node-growth]]).

**Solution**: [[solution-key-value-store]] — attempt first, then read.

**Attempt log**
- [ ] Attempt 1 (date, 40 min, self-graded notes):
