%% trellis:begin %%
# 流（Stream）、任务（Task）与动态表（Dynamic Table）

Snowflake 原生的变更捕获与编排能力，从最底层的偏移量书签到声明式的新鲜度（freshness）SLA。

## Topics
- [[pipelines.stream-offset-bookmark|作为偏移量书签的流（Stream）]]
- [[pipelines.stream-types|流类型（标准 / 仅追加 / 仅插入）]]
- [[pipelines.stream-consumption-and-offset-advance|偏移量仅在消费 DML 内前移]]
- [[pipelines.stream-staleness-and-retention-extension|流的陈旧化与保留期延长]]
- [[pipelines.task-scheduling-cron-and-dag|任务调度与 DAG]]
- [[pipelines.task-conditional-execution|条件式任务执行]]
- [[pipelines.task-serverless-vs-warehouse|无服务器任务与仓库支持型任务]]
- [[pipelines.task-failure-handling|任务失败处理]]
- [[pipelines.dynamictable-target-lag|动态表（Dynamic Table）与 TARGET_LAG]]
- [[pipelines.dynamictable-incremental-vs-full-refresh|增量刷新与全量刷新]]
- [[pipelines.dynamictable-adaptive-refresh|自适应刷新]]
%% trellis:end %%

## Notes
