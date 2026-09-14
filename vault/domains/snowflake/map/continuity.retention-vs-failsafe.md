%% trellis:begin %%
# 时间旅行与故障保护对比
*时间旅行、故障保护与克隆*

默认 1 天（Enterprise 及以上版本最长 90 天）的可查询保留窗口，与随后紧接着的、不可查询的 7 天故障保护（Fail-safe）恢复窗口的对比，以及各自能由谁来发起恢复。

**Requires:** [[txn.mvcc-immutable-partitions|基于不可变微分区的 MVCC]]

**Unlocks:** [[continuity.at-before-statement-syntax|AT / BEFORE 查询语法]], [[continuity.undrop-recovery|UNDROP 恢复]], [[continuity.zero-copy-clone|零拷贝克隆（zero-copy clone）]]

## Readings
- [[snowflak-time-travel|时间旅行(Time Travel):可查询窗口、AT/BEFORE 与 UNDROP]]

## Cards (5)
- [[retention-decrease-background-move]]
- [[retention-dropped-container-overrides-child]]
- [[retention-expiry-moves-to-failsafe]]
- [[retention-min-retention-effective-max]]
- [[retention-period-edition-limits]]
%% trellis:end %%

## Notes
