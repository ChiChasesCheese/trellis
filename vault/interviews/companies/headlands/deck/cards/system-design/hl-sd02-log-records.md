---
id: hl-sd02-log-records
node: system-design.sd02-job-scheduler
type: qa
step: 13
---
## Q
调度器 WAL 里有哪些记录类型？为什么状态机必须是日志的纯函数，「现在几点」怎么处理？

## A
记录：`Scheduled(jobId, fireAt, payloadRef, tenant, epoch)`、`Cancelled(jobId)`、`Dispatched(jobId, attempt, epoch)`（不是必须）、`Fired(jobId, epoch)`（下游确认交付后写）、`Retry(jobId, attempt, nextAt)`、`Dead(jobId)`。

状态机是这些记录的**纯函数** `f(state, record) → state'`，重放同一份日志得到相同状态（事件溯源）。

**「现在是几点」不是状态机的输入**，而是单独的 `Tick(now)` 命令，可以被记录，也可以在测试里被注入。
