---
id: table-types-zero-retention-permanent-vs-transient
node: storage.table-types
type: qa
source: snowflake-docs
---
## Q
把一张表的 `DATA_RETENTION_TIME_IN_DAYS` 设为 0 后修改或删除数据，永久表（permanent）和瞬态表（transient）的历史数据去向有何不同？这说明了两者的什么根本区别？

## A
永久表被修改或删除的数据会由后台进程移入 Fail-safe（故障保护，只能由 Snowflake 恢复的最后一道保护）；瞬态表的这些数据则直接被删除。这体现了瞬态表不享有 Fail-safe 保护：用更少的数据保护换更低的存储成本，适合可以重建的中间数据。后台处理需要一点时间，期间存储指标里的 TIME_TRAVEL_BYTES 仍可能非零。
