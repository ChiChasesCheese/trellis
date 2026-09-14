---
id: mvcc-retention-zero-background-cleanup
node: txn.mvcc-immutable-partitions
type: qa
source: snowflake-docs
---
## Q
把一张表的 `DATA_RETENTION_TIME_IN_DAYS` 设为 0 后，存储指标里的 `TIME_TRAVEL_BYTES` 为什么暂时还不是 0？

## A
保留期为 0 时，被修改或删除的旧版本数据由后台进程处理：永久表（permanent table）的旧数据转入故障保护（Fail-safe），临时性表（transient table）的旧数据直接删除。这个后台过程需要一点时间完成，在此之前旧版本仍占用时间旅行存储，所以 `TIME_TRAVEL_BYTES` 可能暂时非零。
