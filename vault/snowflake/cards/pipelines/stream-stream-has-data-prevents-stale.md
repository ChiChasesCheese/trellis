---
id: stream-stream-has-data-prevents-stale
node: pipelines.stream-staleness-and-retention-extension
type: qa
source: snowflake-docs
---
## Q
一个流的源表很少变化，长期没有数据可消费。除了定期执行 DML 消费，还有什么办法防止它陈旧？过了 `STALE_AFTER` 之后能依赖它吗？

## A
调用 `SYSTEM$STREAM_HAS_DATA` 检查该流：如果流为空、函数返回 FALSE，这次调用也能防止流陈旧。但不要依赖 `STALE_AFTER` 之后的结果：过了该时间戳，流随时可能陈旧（即使没有未消费记录），读取可能仍能成功一段时间，`SYSTEM$STREAM_HAS_DATA` 也可能返回意外结果。应始终在 `STALE_AFTER` 之前消费或检查流。
