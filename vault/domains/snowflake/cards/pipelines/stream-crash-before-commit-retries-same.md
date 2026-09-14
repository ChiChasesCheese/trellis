---
id: stream-crash-before-commit-retries-same
node: pipelines.stream-consumption-and-offset-advance
type: qa
source: snowflake-docs
---
## Q
一个用 MERGE 消费流的作业在事务提交前崩溃。重跑时它会拿到哪些变更？这对管道的正确性意味着什么？

## A
会拿到与上次完全相同的一组变更。偏移量只在读取该流的 DML 事务成功提交时才前移；事务未提交（崩溃或回滚）时，流的位置保持不变。因此消费和写入目标表是原子的：要么变更被写入且偏移量前移，要么两者都没发生，重试不会丢数据，也不会重复消费已提交的批次。
