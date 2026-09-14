%% trellis:begin %%
# 增量刷新与全量刷新
*流（Stream）、任务（Task）与动态表（Dynamic Table）*

动态表何时能仅凭增量数据计算出下一个状态，何时又必须从头重新计算。

**Requires:** [[pipelines.dynamictable-target-lag|动态表（Dynamic Table）与 TARGET_LAG]]

**Unlocks:** [[pipelines.dynamictable-adaptive-refresh|自适应刷新]]

## Readings
- [[snowflak-dynamic-tables|动态表(Dynamic Table):用目标延迟声明代替手写 Stream+Task]]

## Cards (5)
- [[dt-auto-decided-at-creation]]
- [[dt-full-refresh-when-appropriate]]
- [[dt-incremental-why-cheaper]]
- [[dt-refresh-modes-cloze]]
- [[dt-vs-materialized-view-refresh]]
%% trellis:end %%

## Notes
