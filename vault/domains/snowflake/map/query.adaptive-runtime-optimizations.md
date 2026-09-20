%% trellis:begin %%
# 自适应运行时优化
*查询编译与执行*

基于运行时信息做出的决策（例如自适应连接策略选择），利用实际观测到的基数在执行过程中修订计划，而不仅依赖编译期估算。

**Requires:** [[domains/snowflake/map/query.join-strategies-broadcast-shuffle|连接（join）策略]]

## Cards (4)
1. [[adaptive-runtime-join-pruning]]
2. [[adaptive-vs-static-plan-tradeoff]]
3. [[adaptive-where-estimates-break]]
4. [[adaptive-why-defer-join-distribution]]
%% trellis:end %%

## Notes
