---
id: analytics-table-formats
node: analytics.warehouse
type: qa
---
## Q
Iceberg/Delta are "just metadata over Parquet files." What do they actually add that a directory of Parquet files lacks?

## A
- **Atomic commits / snapshots**: a table version is a metadata file listing exactly which data files belong; readers never see half-written jobs (no more `_SUCCESS`-flag conventions).
- **Schema evolution by column ID**: add/rename/drop columns safely without rewriting data files.
- **Hidden partitioning + file-level stats**: queries prune partitions and skip files by min/max column stats without listing directories or knowing the partition scheme.
- **Time travel**: query any retained snapshot; roll back a bad write by re-pointing.

In short: they turn files into a **transactional table abstraction** any engine can share.

## Q zh
Iceberg/Delta 是"仅在 Parquet 文件上的元数据"。它们实际添加什么 Parquet 文件目录缺乏？

## A zh
- **原子提交 / 快照**：table 版本是元数据文件，列举精确哪些数据文件属于；reader 永远看不到半写的 job（没有更多`_SUCCESS`-flag 惯例）。
- **按 column ID 的 schema 演化**：安全添加/重命名/删除列，不重写数据文件。
- **隐藏分区 + 文件级统计**：查询 prune partition 和按 min/max 列统计跳过文件，不列目录或知道 partition scheme。
- **时间旅行**：查询任何保留的快照；通过重新指向回滚一个坏写。

总之：它们把文件变成**事务性 table 抽象**任何引擎可以共享。
