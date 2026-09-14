---
nodes:
- pipelines.task-scheduling-cron-and-dag
- pipelines.task-serverless-vs-warehouse
- pipelines.task-failure-handling
- pipelines.task-conditional-execution
title: 任务(Task):调度、算力模型与失败处理
corpus: snowflake-docs
section: 22-tasks-intro
url: https://docs.snowflake.com/en/user-guide/tasks-intro
tags:
- canonical
---

# 任务(Task):调度、算力模型与失败处理

Task 可以按固定时间间隔或 CRON 表达式调度,也可以组成任务图(task graph)串联成流水线,最多支持 100 个任务节点。算力上二选一:serverless 模式由 Snowflake 自动预测并分配资源(依据近期运行历史动态调节仓库尺寸上下限);用户托管模式则绑定固定仓库,适合已经有稳定并发负载的场景。可以配合 SYSTEM$STREAM_HAS_DATA() 让任务在上游流为空时直接跳过本次运行,避免空转浪费信用点。失败处理上,SUSPEND_TASK_AFTER_NUM_FAILURES 可在连续失败若干次后自动挂起任务,TASK_AUTO_RETRY_ATTEMPTS 则可以让失败的任务自动重试。读完应能设计一条“调度—条件判断—失败重试”齐全的数据管道。

%% trellis:begin %%
## Source
[Open the original ↗](https://docs.snowflake.com/en/user-guide/tasks-intro)

## Archived copy
![[snowflak-tasks-clip]]
%% trellis:end %%
