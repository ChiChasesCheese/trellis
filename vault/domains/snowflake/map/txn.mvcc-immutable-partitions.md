%% trellis:begin %%
# 基于不可变微分区的 MVCC
*事务与并发控制*

一次写入从不就地修改微分区，而是生成一个新的表版本，引用新写入的分区与未变化的分区。

**Requires:** [[storage.micro-partition-format|微分区（micro-partition）格式]], [[txn.snapshot-isolation|隔离级别：READ COMMITTED 与一致性读]]

**Unlocks:** [[txn.optimistic-concurrency-conflicts|写并发：表级锁与写冲突]], [[continuity.retention-vs-failsafe|时间旅行与故障保护对比]], [[pipelines.stream-offset-bookmark|作为偏移量书签的流（Stream）]]

## Readings
- [[snowflak-time-travel|时间旅行(Time Travel):可查询窗口、AT/BEFORE 与 UNDROP]]

## Cards (5)
- [[mvcc-dml-preserves-previous-version]]
- [[mvcc-high-churn-storage-cost]]
- [[mvcc-historical-query-uses-current-schema]]
- [[mvcc-long-query-delays-failsafe-transition]]
- [[mvcc-retention-zero-background-cleanup]]
%% trellis:end %%

## Notes
