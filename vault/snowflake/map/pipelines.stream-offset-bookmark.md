%% trellis:begin %%
# 作为偏移量书签的流（Stream）
*流（Stream）、任务（Task）与动态表（Dynamic Table）*

一个 Stream 是指向表版本历史中某一点的指针，而不是数据的副本；查询它返回的是自上次消费以来的净变化。

**Requires:** [[txn.mvcc-immutable-partitions|基于不可变微分区的 MVCC]]

**Unlocks:** [[pipelines.stream-types|流类型（标准 / 仅追加 / 仅插入）]], [[pipelines.stream-consumption-and-offset-advance|偏移量仅在消费 DML 内前移]], [[pipelines.stream-staleness-and-retention-extension|流的陈旧化与保留期延长]], [[pipelines.task-scheduling-cron-and-dag|任务调度与 DAG]], [[pipelines.dynamictable-target-lag|动态表（Dynamic Table）与 TARGET_LAG]]

## Readings
- [[snowflak-streams|流对象(Stream)的偏移量、类型与消费语义]]

## Cards (5)
- [[stream-changes-clause-alternative]]
- [[stream-multiple-streams-cheap]]
- [[stream-offset-between-versions]]
- [[stream-row-change-metadata-columns]]
- [[stream-stores-only-offset]]
%% trellis:end %%

## Notes
