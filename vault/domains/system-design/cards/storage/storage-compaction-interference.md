---
id: storage-compaction-interference
node: storage.internals.tradeoffs
type: qa
---
## Q
An LSM store benchmarks beautifully, then in production shows periodic latency spikes and, under sustained ingest, throughput collapse. Explain the compaction-interference mechanism behind both symptoms, and what engines do about it.

## A
The disk's finite bandwidth is **shared** between the foreground write path (WAL + memtable flushes) and background compaction — and the read path competes for the same disk and page cache.

- **Latency spikes**: when a big compaction runs, reads suddenly contend for I/O and evicted cache; at high percentiles queries queue behind compaction bursts. The benchmark missed it because short runs barely trigger compaction.
- **Collapse under sustained ingest**: incoming writes are *cheaper* than compaction (each ingested byte must later be rewritten multiple times), so ingest can outrun compaction indefinitely. The backlog of unmerged SSTables grows without bound → reads must check ever more files → read amplification climbs until the system is effectively broken.

Engine responses: **throttle/stall writes** when pending compaction debt crosses thresholds (RocksDB write stalls) — deliberately trading peak ingest for stability — plus rate-limited compaction I/O. Operationally: monitor pending-compaction bytes and file counts per level, not just write QPS.

## Q zh
一个 LSM 存储在基准测试里表现漂亮，上了生产却出现周期性延迟尖刺，且在持续写入下吞吐崩塌。解释这两个症状背后的 compaction 干扰机制，以及引擎的应对手段。

## A zh
磁盘有限的带宽是被**共享**的：前台写路径（WAL + memtable flush）和后台 compaction 分同一份 — 读路径还要争同一块磁盘和 page cache。

- **延迟尖刺**：大 compaction 运行时，读请求突然要争抢 I/O 和被挤掉的缓存；在高分位上，查询排在 compaction 突发后面。基准测试没测出来，是因为短时间跑几乎不触发 compaction。
- **持续写入下的崩塌**：接收写入比 compaction *便宜*（每个写入的字节之后还要被重写多次），所以写入速度可以无限期跑赢 compaction。未合并 SSTable 的积压无界增长 → 读取要检查越来越多的文件 → 读放大（read amplification）攀升，直到系统实际上不可用。

引擎的应对：当待处理 compaction 债务越过阈值时**限流/暂停写入**（RocksDB 的 write stall）— 有意用峰值写入换稳定性 — 外加对 compaction I/O 限速。运维上：监控 pending compaction 字节数和每层文件数，而不只是写 QPS。
