---
id: analytics-lakehouse-compaction
node: analytics.warehouse
type: qa
---
## Q
A streaming pipeline commits to an Iceberg/Delta table every minute. What degrades over time, and what's the maintenance answer?

## A
**Small-file buildup**: each commit writes tiny Parquet files, so queries pay per-file overhead — metadata/footer reads, one object-store GET each (~tens of ms first-byte), poor compression, less effective min/max pruning. Thousands of small files can dominate query time.

Answer: background **compaction** (`OPTIMIZE` / rewrite-data-files) merges small files into large ones (target ~128MB–1GB), optionally clustering/sorting by common filter keys; plus expiring old snapshots so dead files get deleted.

Same compaction tax as LSM-trees — moved to the lakehouse layer, and it's your job to schedule it.

## Q zh
流管道每分钟提交到 Iceberg/Delta 表。什么随时间降低，维护答案是什么？

## A zh
**小文件堆积**：每个提交写小 Parquet 文件，所以查询支付 per-file 开销 — 元数据/footer 读、一个对象存储 GET 每个（~数十 ms first-byte）、糟糕压缩、较少有效 min/max 修剪。数千个小文件可能支配查询时间。

答案：后台**compaction**（`OPTIMIZE` / rewrite-data-files）合并小文件到大文件（目标 ~128MB–1GB），可选地按常见过滤 key 聚类/排序；加上过期旧快照所以死文件被删除。

与 LSM-tree 相同的 compaction 税 — 移到 lakehouse 层，是你的工作安排。
