%% trellis:begin %%
# 动态表（Dynamic Table）与 TARGET_LAG
*流（Stream）、任务（Task）与动态表（Dynamic Table）*

声明一个新鲜度 SLA，而不必手写过去用来实现它的 Stream+Task+MERGE 组合，以及调度器如何据此推导出刷新节奏。

**Requires:** [[domains/snowflake/map/pipelines.stream-offset-bookmark|作为偏移量书签的流（Stream）]], [[domains/snowflake/map/pipelines.task-scheduling-cron-and-dag|任务调度与 DAG]]

**Unlocks:** [[domains/snowflake/map/pipelines.dynamictable-incremental-vs-full-refresh|增量刷新与全量刷新]]

## Readings
- [[snowflak-dynamic-tables|动态表(Dynamic Table):用目标延迟声明代替手写 Stream+Task]]

## Cards (6)
- [[dt-cost-categories]]
- [[dt-declarative-vs-stream-task]]
- [[dt-pipeline-consistent-snapshot]]
- [[dt-scheduler-disable-external]]
- [[dt-target-lag-downstream]]
- [[dt-target-lag-not-guarantee]]
%% trellis:end %%

## Notes
