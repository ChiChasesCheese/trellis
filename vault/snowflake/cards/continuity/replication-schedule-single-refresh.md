---
id: replication-schedule-single-refresh
node: continuity.replication-and-failover
type: qa
source: snowflake-docs
---
## Q
复制组设置 `REPLICATION_SCHEDULE` 为每 10 分钟一次，某次刷新在 12:01 开始却跑了 15 分钟。下一次刷新何时开始？

## A
下次刷新本应按上次刷新开始时间加间隔排在 12:11，但 Snowflake 保证任一时刻只执行一个刷新：若到点时上一次仍在运行，下一次会推迟到当前刷新完成（12:16）时才开始。因此复制延迟（RPO，可容忍的数据丢失窗口）不仅取决于调度间隔，也取决于单次刷新耗时。
