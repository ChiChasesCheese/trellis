---
id: undrop-restores-in-place-latest-state
node: continuity.undrop-recovery
type: qa
source: snowflake-docs
---
## Q
在 Snowflake 中 DROP 一张表之后，它的数据会立刻被删除吗？`UNDROP TABLE` 会把它恢复成什么状态？

## A
不会立刻删除。被删除的表、模式或数据库会在其数据保留期（data retention period）内继续保留，期间可以恢复；一旦转入故障保护（Fail-safe）就无法再恢复。`UNDROP` 把对象原地恢复（不是创建新对象）到 DROP 命令执行前的最新状态。
