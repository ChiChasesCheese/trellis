---
id: storage-btree-vs-lsm
node: storage.internals.tradeoffs
type: qa
---
## Q
When do you pick an LSM-tree engine (RocksDB, Cassandra) over a B-tree engine (Postgres, InnoDB), and what do you pay for it?

## A
Pick LSM for **write-heavy** workloads: writes are sequential appends (memtable + WAL, flushed to sorted SSTables), so ingest throughput far exceeds a B-tree's random in-place page writes.

You pay with:
- **Read amplification** — a point read may check the memtable plus several SSTable levels (bloom filters mitigate).
- **Compaction** — background rewriting that steals I/O/CPU and causes latency spikes when it falls behind.

B-trees win on read-heavy/mixed workloads and give predictable point/range read latency; each key lives in exactly one place.

## Q zh
什么时候选 LSM-tree 引擎（RocksDB、Cassandra）而不是 B-tree 引擎（Postgres、InnoDB），代价是什么？

## A zh
对于**写密集**工作负载选 LSM：写是顺序 append（memtable + WAL，刷到已排序的 SSTable），所以摄入吞吐远超 B-tree 的随机原地页写。

你需要付出代价：
- **Read amplification**——点查可能检查 memtable 加多个 SSTable 层（bloom filter 可以缓解）。
- **Compaction**——后台重写，抢占 I/O/CPU，落后时会导致延迟尖刺。

B 树在读密集/混合工作负载中胜出，提供可预测的点/范围查延迟；每个键恰好存在一处。
