%% trellis:begin %%
# 连接（join）策略
*查询编译与执行*

广播连接（broadcast join）与洗牌连接（shuffle/hash-repartition join）的对比，以及优化器据以选择其一的数据量启发式规则。

**Core** — part of the first pass through this subject.

**Requires:** [[domains/snowflake/map/query.dag-execution-model|DAG 执行模型]]

**Unlocks:** [[domains/snowflake/map/query.adaptive-runtime-optimizations|自适应运行时优化]]

## Cards (5)
1. [[join-broadcast-mechanism]]
2. [[join-build-probe-and-join-filter]]
3. [[join-choice-heuristic]]
4. [[join-shuffle-mechanism]]
5. [[join-strategy-failure-modes]]
%% trellis:end %%

## Notes
