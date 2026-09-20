%% trellis:begin %%
# Distributed Key-Value Store
*Design Problems / Building Blocks & Warm-ups*

Partitioning, replication, quorums, conflict resolution and repair in a Dynamo-style store.

**Requires:** [[domains/system-design/map/distributed.replication.leaderless|Leaderless & Quorums]], [[domains/system-design/map/distributed.partitioning.schemes|Hash vs Range]]

## Readings
- [[solution-key-value-store|设计题解：分布式键值存储（Distributed Key-Value Store，Dynamo 风格）]]
- [[src-dynamo-paper-key-value-store|Dynamo: Amazon's Highly Available Key-value Store]]
- [[src-redis-cluster-spec|Redis cluster specification]]

## Drills
- [[design-key-value-store|Drill: Design a highly-available distributed key-value store]]

## Cards (8)
1. [[problems-key-value-store-qps-bound-not-storage-bound]]
2. [[problems-key-value-store-consistent-hashing-vnode-choice]]
3. [[problems-key-value-store-quorum-availability-math]]
4. [[problems-key-value-store-sloppy-quorum-hinted-handoff]]
5. [[problems-key-value-store-vector-clock-vs-lww]]
6. [[problems-key-value-store-merkle-tree-anti-entropy]]
7. [[problems-key-value-store-gossip-convergence-log-n]]
8. [[problems-key-value-store-10x-node-growth]]
%% trellis:end %%

## Notes
