---
id: distributed-dynamic-split-merge
node: distributed.partitioning.rebalancing
type: qa
---
## Q
How does dynamic (split/merge) partitioning work, what triggers each operation, and what's the pitfall on an empty database?

## A
Ranges are split when a partition exceeds a size or load threshold — HBase regions (~10 GB), CockroachDB ranges (~512 MiB), DynamoDB partitions (10 GB or when throughput demands it). The split is a **metadata operation first**: the range is cut at a chosen mid-key into two ranges owned by the same node, and only then may one half be *moved* to another node. Merges run the other way when adjacent ranges shrink (after mass deletes), to stop metadata from fragmenting.

Pitfall: a **fresh database starts as one partition on one node** — all writes hit a single machine until the first split completes, so a load test or a bulk load looks catastrophically slow. Fix: **pre-split** at creation using known key boundaries (HBase pre-splitting, Cockroach split points, DynamoDB's older parallel-load guidance). Advantage over fixed counts: the partition count tracks data volume automatically, so it works from 1 GB to 100 TB.

## Q zh
动态（分裂/合并）分区是怎么工作的？各自由什么触发？在一个空数据库上有什么坑？

## A zh
当一个分区超过大小或负载阈值时就会分裂——HBase 的 region（约 10 GB）、CockroachDB 的 range（约 512 MiB）、DynamoDB 的分区（10 GB，或吞吐量需要时）。分裂**首先是一次元数据操作**：range 在选定的中间 key 处被切成两个 range，仍然归同一个节点所有，只有之后其中一半才可能被*移动*到另一个节点。合并则反过来，在相邻 range 缩小时（比如大批量删除之后）运行，防止元数据碎片化。

坑在于：一个**全新的数据库一开始就是单个节点上的单个分区**——在第一次分裂完成之前，所有写入都打在同一台机器上，所以压测或批量导入看起来会慢得离谱。修复办法：在创建时用已知的 key 边界**预分裂**（HBase 的 pre-splitting、Cockroach 的 split points、DynamoDB 早期的并行导入指南）。相比固定数量分区的优势：分区数会自动跟着数据量走，所以从 1 GB 到 100 TB 都能用。
