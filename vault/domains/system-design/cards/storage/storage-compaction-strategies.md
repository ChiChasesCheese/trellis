---
id: storage-compaction-strategies
node: storage.internals.lsm
type: qa
---
## Q
Size-tiered vs leveled compaction in an LSM engine: how does each organize SSTables, and which workload picks which?

## A
- **Size-tiered** (Cassandra STCS): wait for ~4 similar-sized SSTables, merge into one bigger; tiers of ever-larger files. Each byte is rewritten few times (**low write amp**) but key ranges overlap across many files (**high read/space amp** — worst case ~2x space during a merge).
- **Leveled** (RocksDB/LevelDB): levels L1, L2... each ~10x larger, with **non-overlapping** key ranges within a level; a lookup checks at most one file per level. Low read/space amp, but data is rewritten into each level it descends through (**write amp ~10 per level**).

Pick size-tiered for write-heavy/append-mostly (logs, time-series); leveled when reads and space matter more than peak ingest. See [[storage-amplification-triangle]].

## Q zh
LSM 引擎中 size-tiered vs leveled 压实：各自如何组织 SSTable，哪种工作负载选哪种？

## A zh
- **Size-tiered**（Cassandra STCS）：等待 ~4 个相似大小的 SSTable，合并成一个更大的；分层递增文件。每字节重写次数少（**低 write amp**），但键范围跨多个文件重叠（**高 read/space amp**——最坏情况合并时 ~2 倍空间）。
- **Leveled**（RocksDB/LevelDB）：层级 L1、L2...各约 10 倍大，层内**非重叠**的键范围；查询最多检查每层一个文件。低 read/space amp，但数据在它下降的每个层都被重写（**write amp ~10 per level**）。

写密集/仅 append 工作负载（日志、时间序列）选 size-tiered；读和空间比峰值摄入更重要时选 leveled。见 [[storage-amplification-triangle]]。
