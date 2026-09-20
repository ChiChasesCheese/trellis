---
id: problems-key-value-store-consistent-hashing-vnode-choice
node: problems.foundations.key-value-store
type: qa
step: 2
tags: [grown]
---
## Q
In a distributed key-value store that only needs point lookups (no range scans), why is consistent hashing with virtual nodes chosen over both range partitioning and a fixed number of hash partitions (`hash(key) % P`)?

## A
Range partitioning enables range scans this store doesn't need, and creates hotspots on sequentially-increasing keys that need auto-splitting to fix. Fixed hash partitioning (`% P`) is simple but P is fixed at cluster creation: adding a physical node changes almost every key's target partition under modulo arithmetic, forcing a full remap. Consistent hashing places both keys and nodes on a ring so a key belongs to the next node clockwise; adding one physical node only moves the range between it and its predecessor. Because one virtual node per physical node causes uneven load at small node counts, each physical node is given multiple virtual nodes (tokens) on the ring to average load out.

## Q zh
在一个只需要点查（不需要范围扫描）的分布式键值存储中，为什么选择带虚拟节点的一致性哈希，而不是范围分区或固定数量的哈希分区（`hash(key) % P`）？

## A zh
范围分区能支持这个存储不需要的范围扫描，并且会在递增 key 上产生需要自动分裂来修复的热点。固定哈希分区（`% P`）简单，但 P 在建集群时就定死：取模运算下，新增一个物理节点会改变几乎每个 key 的目标分区，逼出一次全量重映射。一致性哈希把 key 和节点都放到同一个环上，key 归属于顺时针方向下一个节点；只加一个物理节点时，只有它和前一个节点之间的那段区间需要迁移。因为节点数少时每个物理节点只对应环上一个点会导致负载不均，所以每个物理节点在环上持有多个虚拟节点（token）来平均负载。
