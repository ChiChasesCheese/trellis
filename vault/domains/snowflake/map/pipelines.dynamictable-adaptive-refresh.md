%% trellis:begin %%
# 自适应刷新
*流（Stream）、任务（Task）与动态表（Dynamic Table）*

检测到上游变化大到增量刷新反而比重新初始化更慢时，自动切换刷新策略。

**Requires:** [[domains/snowflake/map/pipelines.dynamictable-incremental-vs-full-refresh|增量刷新与全量刷新]]

## Readings
- [[snowflak-dynamic-tables|动态表(Dynamic Table):用目标延迟声明代替手写 Stream+Task]]

## Cards (4)
- [[dt-adaptive-backfill-scenario]]
- [[dt-adaptive-definition]]
- [[dt-adaptive-vs-auto]]
- [[dt-custom-incremental-escape-hatch]]
%% trellis:end %%

## Notes
