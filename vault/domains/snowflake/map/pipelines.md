%% trellis:begin %%
# 流（Stream）、任务（Task）与动态表（Dynamic Table）

Snowflake 原生的变更捕获与编排能力，从最底层的偏移量书签到声明式的新鲜度（freshness）SLA。

## Topics
- [[domains/snowflake/map/pipelines.stream-offset-bookmark|作为偏移量书签的流（Stream）]]
- [[domains/snowflake/map/pipelines.stream-types|流类型（标准 / 仅追加 / 仅插入）]]
- [[domains/snowflake/map/pipelines.stream-consumption-and-offset-advance|偏移量仅在消费 DML 内前移]]
- [[domains/snowflake/map/pipelines.stream-staleness-and-retention-extension|流的陈旧化与保留期延长]]
- [[domains/snowflake/map/pipelines.task-scheduling-cron-and-dag|任务调度与 DAG]]
- [[domains/snowflake/map/pipelines.task-conditional-execution|条件式任务执行]]
- [[domains/snowflake/map/pipelines.task-serverless-vs-warehouse|无服务器任务与仓库支持型任务]]
- [[domains/snowflake/map/pipelines.task-failure-handling|任务失败处理]]
- [[domains/snowflake/map/pipelines.dynamictable-target-lag|动态表（Dynamic Table）与 TARGET_LAG]]
- [[domains/snowflake/map/pipelines.dynamictable-incremental-vs-full-refresh|增量刷新与全量刷新]]
- [[domains/snowflake/map/pipelines.dynamictable-adaptive-refresh|自适应刷新]]
%% trellis:end %%

## Notes
