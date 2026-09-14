---
id: task-stream-has-data-prevents-staleness
node: pipelines.task-conditional-execution
type: qa
source: snowflake-docs
---
## Q
一个带 `WHEN SYSTEM$STREAM_HAS_DATA(...)` 条件的任务，所监控的流连续数周都没有数据，任务一直跳过。这个流会因为长期未被消费而陈旧（stale）吗？

## A
通常不会。在流为空、`SYSTEM$STREAM_HAS_DATA` 返回 FALSE 的情况下，调用该函数本身就能防止流变得陈旧，所以条件检查在跳过运行的同时也在「保活」这个流。但如果流中确实有数据，就必须在 `STALE_AFTER` 时间之前通过 DML 消费它，否则仍可能陈旧。
