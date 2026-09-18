%% trellis:begin %%
# 任务调度与 DAG
*流（Stream）、任务（Task）与动态表（Dynamic Table）*

由 CRON 表达式或固定间隔调度的 Task，可组合成最多包含 100 个任务的依赖图（task graph）。

**Requires:** [[domains/snowflake/map/pipelines.stream-offset-bookmark|作为偏移量书签的流（Stream）]]

**Unlocks:** [[domains/snowflake/map/pipelines.task-conditional-execution|条件式任务执行]], [[domains/snowflake/map/pipelines.task-serverless-vs-warehouse|无服务器任务与仓库支持型任务]], [[domains/snowflake/map/pipelines.task-failure-handling|任务失败处理]], [[domains/snowflake/map/pipelines.dynamictable-target-lag|动态表（Dynamic Table）与 TARGET_LAG]]

## Readings
- [[snowflak-tasks|任务(Task):调度、算力模型与失败处理]]

## Cards (6)
- [[task-created-suspended]]
- [[task-graph-root-and-children]]
- [[task-overlap-skip-scheduled-run]]
- [[task-runs-as-system-service]]
- [[task-schedule-interval-vs-cron]]
- [[task-version-pinned-at-run-start]]
%% trellis:end %%

## Notes
