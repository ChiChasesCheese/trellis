%% trellis:begin %%
# 连接（join）策略
*查询编译与执行*

广播连接（broadcast join）与洗牌连接（shuffle/hash-repartition join）的对比，以及优化器据以选择其一的数据量启发式规则。

**Requires:** [[query.dag-execution-model|DAG 执行模型]]

**Unlocks:** [[query.adaptive-runtime-optimizations|自适应运行时优化]]

## Cards (5)
- [[join-broadcast-mechanism]]
- [[join-build-probe-and-join-filter]]
- [[join-choice-heuristic]]
- [[join-shuffle-mechanism]]
- [[join-strategy-failure-modes]]
%% trellis:end %%

## Notes
