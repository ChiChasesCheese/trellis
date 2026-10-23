---
id: hl-javaq-j-q45-say60
node: java-questions.j-storage
type: qa
step: 11
---
## Q
用英文 60 秒回答：Distributed storage: replication, consistency and the trade-offs between LSM trees and B-trees. What would you think about when designing a storage layer for research data?

## A
结构：从访问模式出发 → B 树 vs LSM（写路径、读放大、合并）→ 同步复制加 Raft vs 异步复制 → 研究数据写一次、批量扫描，适合不可变分区文件加元数据索引 → 一开始就做监控。

> "I'd start from the access pattern: read/write ratio, sequential versus random, latency targets, consistency and failure tolerance. A B-tree updates pages in place so reads and range scans are good but writes are random; an LSM tree turns writes into sequential appends to a log and memtable, flushes sorted immutable files and compacts in the background, so writes are cheap while reads and compaction cost more - Bloom filters help the reads. Across machines I'd decide between synchronous replication through a consensus protocol like Raft - strong consistency, write latency bounded by the slowest majority's fsync and network - and asynchronous replication that's faster but can lose the latest writes. For research data, which is mostly write-once, append-heavy and scanned in bulk, immutable partitioned files with a metadata index tends to fit better than a general transactional store. I'd also build the monitoring in from the start."
